from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.chat_chain import ask_ai
from backend.retriever import get_retriever
from backend.cart_wishlist import (
    add_to_cart, remove_from_cart, update_cart_quantity, get_cart, clear_cart,
    add_to_wishlist, remove_from_wishlist, get_wishlist, move_wishlist_to_cart
)
from fastapi.middleware.cors import CORSMiddleware

import json
from pathlib import Path
import logging
from rapidfuzz import fuzz, process

# -------------------- Logging Setup --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("backend.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend ka URL yahan dal sakte ho e.g., ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever = None
products_cache = {}

class ChatRequest(BaseModel):
    query: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 2

# -------------------- Utility --------------------
def success_response(message, data=None):
    return {"status": "success", "message": message, "data": data}

def error_response(message):
    return {"status": "error", "message": message}

# -------------------- Global Error Handler --------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Error: {str(exc)}", exc_info=True)
    return JSONResponse(status_code=500, content=error_response("Internal Server Error"))

# -------------------- Startup --------------------
@app.on_event("startup")
def load_retriever():
    global retriever, products_cache
    retriever = get_retriever()
    logging.info("Retriever loaded successfully!")

    file_path = Path(__file__).parent / "data/products.json"
    with open(file_path, "r", encoding="utf-8") as f:
        products_cache = {p["product_id"]: p for p in json.load(f)}
    logging.info(f"Loaded {len(products_cache)} products into cache.")

# -------------------- Root --------------------
@app.get("/")
def read_root():
    return success_response("AI Shopping Assistant Backend is running!")

# -------------------- Chat --------------------
# @app.post("/chat")
# def chat(request: ChatRequest):
#     response = ask_ai(request.query)
#     return success_response("AI response generated", {
#         "answer": response["result"],
#         "sources": [doc.metadata for doc in response["source_documents"]]
#     })

@app.post("/chat")
def chat(request: ChatRequest):  # ChatRequest me 'question' field rakho
    response = ask_ai(request.query)
    return success_response("AI response generated", {
        "answer": response["result"],
        "sources": [doc.metadata for doc in response["source_documents"]]
    })
# -------------------- Get All Products --------------------
@app.get("/products")
def get_products():
    return success_response("Product list fetched", list(products_cache.values()))

# -------------------- Get Product by ID --------------------
@app.get("/products/{product_id}")
def get_product_by_id(product_id: str):
    if product_id in products_cache:
        return success_response("Product found", products_cache[product_id])
    return error_response("Product not found")

# -------------------- Search Products --------------------
@app.post("/search")
def search_products(query: str = Query(...), top_k: int = 5, category: str = None, min_price: float = None, max_price: float = None):
    docs = retriever.invoke(query)

    file_path = Path(__file__).parent / "data/products.json"
    with open(file_path, "r", encoding="utf-8") as f:
        products = {p["product_id"]: p for p in json.load(f)}

    results = []
    query_lower = query.lower()

    # 1. Exact/substring match in product name
    for doc in docs:
        pid = doc.metadata.get("product_id")
        if pid in products:
            product = products[pid]
            if query_lower in product["product_name"].lower():
                results.append(product)

    # 2. Fuzzy match if not enough results
    if len(results) < top_k:
        candidates = [p for p in products.values() if p not in results]
        fuzzy_matches = process.extract(
            query,
            [(p["product_id"], p["product_name"] + " " + p.get("about_product", "")) for p in candidates],
            scorer=fuzz.token_sort_ratio,
            limit=top_k * 2
        )
        for (pid, _), score, _ in fuzzy_matches:
            if score >= 70 and products[pid] not in results:
                results.append(products[pid])
            if len(results) >= top_k:
                break

    # 3. Apply filters if provided
    def passes_filters(product):
        if category and product.get("category") and product["category"].lower() != category.lower():
            return False
        if min_price is not None and float(product.get("price", 0)) < min_price:
            return False
        if max_price is not None and float(product.get("price", 0)) > max_price:
            return False
        return True
    filtered_results = [p for p in results if passes_filters(p)]

    # 4. Suggestions if no results
    suggestions = []
    if not filtered_results:
        # Suggest similar product names
        all_names = [p["product_name"] for p in products.values()]
        suggestions = [s for s, score, _ in process.extract(query, all_names, scorer=fuzz.token_sort_ratio, limit=3) if score >= 60]

    return {"products": filtered_results[:top_k], "suggestions": suggestions}


# -------------------- Recommendations --------------------
@app.get("/recommendations/{product_id}")
def recommend_products(product_id: str, top_k: int = 5):
    if product_id not in products_cache:
        return error_response("Product not found")

    try:
        p = products_cache[product_id]
        parts = [
            p.get('product_name', ''),
            p.get('about_product', ''),
            p.get('category', ''),
            p.get('brand', '') or p.get('manufacturer', ''),
        ]
        # include optional features/tags/specs if present
        for k in ('features', 'tags', 'specs'):
            v = p.get(k)
            if isinstance(v, list):
                parts.append(', '.join([str(x) for x in v]))
            elif isinstance(v, dict):
                parts.append(', '.join([f"{kk}: {vv}" for kk, vv in v.items()]))
            elif v:
                parts.append(str(v))
        query_text = ' '.join([str(x) for x in parts if x])
        docs = retriever.vectorstore.as_retriever(
            search_kwargs={"k": top_k + 1}
        ).invoke(query_text)

        results = []
        seen = set()
        for doc in docs:
            pid = doc.metadata.get("product_id")
            if pid != product_id and pid in products_cache and pid not in seen:
                results.append(products_cache[pid])
                seen.add(pid)
            if len(results) >= top_k:
                break

        return success_response("Recommendations fetched", results)
    except Exception as e:
        logging.error(f"Recommendations failed: {e}")
        return error_response("Recommendations failed")

# -------------------- Query-based Recommendations --------------------
@app.get("/recommendations/by-query")
def recommend_by_query(query: str = Query(...), top_k: int = 6):
    try:
        docs = retriever.invoke(query)
        results = []
        seen = set()
        for doc in docs:
            pid = doc.metadata.get("product_id")
            if pid in products_cache and pid not in seen:
                results.append(products_cache[pid])
                seen.add(pid)
            if len(results) >= top_k:
                break
        return success_response("Query recommendations fetched", results)
    except Exception as e:
        logging.error(f"Query recommendations failed: {e}")
        return error_response("Query recommendations failed")

# -------------------- CART APIs --------------------
@app.post("/cart/add")
def api_add_to_cart(user_id: str, product_id: str, quantity: int = 1):
    try:
        return success_response("Product added to cart", add_to_cart(user_id, product_id, quantity))
    except ValueError as e:
        return error_response(str(e))

@app.post("/cart/remove")
def api_remove_from_cart(user_id: str, product_id: str):
    return success_response("Product removed from cart", remove_from_cart(user_id, product_id))

@app.post("/cart/update")
def api_update_cart_quantity(user_id: str, product_id: str, quantity: int):
    try:
        return success_response("Cart updated", update_cart_quantity(user_id, product_id, quantity))
    except ValueError as e:
        return error_response(str(e))

@app.get("/cart/{user_id}")
def api_get_cart(user_id: str):
    return success_response("Cart fetched", get_cart(user_id))

@app.post("/cart/clear")
def api_clear_cart(user_id: str):
    return success_response("Cart cleared", clear_cart(user_id))

# -------------------- WISHLIST APIs --------------------
@app.post("/wishlist/add")
def api_add_to_wishlist(user_id: str, product_id: str):
    return success_response("Product added to wishlist", add_to_wishlist(user_id, product_id))

@app.post("/wishlist/remove")
def api_remove_from_wishlist(user_id: str, product_id: str):
    return success_response("Product removed from wishlist", remove_from_wishlist(user_id, product_id))

@app.get("/wishlist/{user_id}")
def api_get_wishlist(user_id: str):
    return success_response("Wishlist fetched", get_wishlist(user_id))

@app.post("/wishlist/move-to-cart")
def api_move_wishlist_to_cart(user_id: str, product_id: str, quantity: int = 1):
    return success_response("Product moved from wishlist to cart",
                            move_wishlist_to_cart(user_id, product_id, quantity))
