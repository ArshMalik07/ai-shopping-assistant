# # from fastapi import FastAPI
# # from pydantic import BaseModel
# # from fastapi.middleware.cors import CORSMiddleware
# # from backend.chat_chain import ask_ai

# # # Step 1: Initialize FastAPI
# # app = FastAPI(title="AI Shopping Assistant API")

# # # Step 2: Enable CORS (so frontend can access API)
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],  # Change to specific domain in production
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Step 3: Create request model
# # class ChatRequest(BaseModel):
# #     query: str

# # # Step 4: Root route (health check)
# # @app.get("/")
# # def read_root():
# #     return {"message": "AI Shopping Assistant Backend is running!"}

# # # Step 5: Chat route
# # @app.post("/chat")
# # def chat_endpoint(request: ChatRequest):
# #     answer = ask_ai(request.query)
# #     return {"query": request.query, "response": answer}



# # backend/main.py

# from fastapi import FastAPI
# from pydantic import BaseModel
# from backend.chat_chain import ask_ai
# from backend.retriever import get_retriever
# import json
# from pathlib import Path

# app = FastAPI()

# # Global retriever
# retriever = None

# class ChatRequest(BaseModel):
#     query: str

# class SearchRequest(BaseModel):
#     query: str
#     top_k: int = 2

# @app.on_event("startup")
# def load_retriever():
#     """
#     Server start hone par retriever ek hi baar load hoga
#     """
#     global retriever
#     retriever = get_retriever()
#     print("Retriever loaded successfully!")

# @app.get("/")
# def read_root():
#     return {"message": "AI Shopping Assistant Backend is running!"}

# @app.post("/chat")
# def chat(request: ChatRequest):
#     response = ask_ai(request.query)
#     return {
#         "answer": response["result"],
#         "sources": [doc.metadata for doc in response["source_documents"]]
#     }

# @app.get("/products")
# def get_products():
#     file_path = Path(__file__).parent/"data/products.json"
#     with open(file_path, "r", encoding="utf-8") as f:
#         products = json.load(f)
#     return products

# @app.get("/products/{product_id}")
# def get_product_by_id(product_id: str):
#     file_path = Path(__file__).parent/"data/products.json"
#     with open(file_path, "r", encoding="utf-8") as f:
#         products = json.load(f)

#     for product in products:
#         if product["product_id"] == product_id:
#             return product
#     return {"error": "Product not found"}

# # @app.post("/search")
# # def search_products(request: SearchRequest):
# #     file_path = Path(__file__).parent/"data/products.json"
# #     with open(file_path, "r", encoding='utf-8') as f:
# #         products = {p["product_id"]: p for p in json.load(f)}

# #     docs = retriever.get_relevant_documents(request.query)
# #     results = []
# #     for doc in docs[:request.top_k]:
# #         pid = doc.metadata.get("product_id")
# #         if pid in products:
# #             results.append(products[pid])

# #     return results

# # @app.get("/recommendations/{product_id}")
# # def recommend_products(product_id: str, top_k: int = 5):
# #     file_path = Path(__file__).parent / "data/products.json"
# #     with open(file_path, "r", encoding="utf-8") as f:
# #         products = {p["product_id"]: p for p in json.load(f)}

# #     if product_id not in products:
# #         return {"error": "Product not found"}

# #     product = products[product_id]
# #     query_text = product["product_name"] + " " + product["about_product"]

# #     docs = retriever.get_relevant_documents(query_text)
# #     results = []
# #     for doc in docs:
# #         pid = doc.metadata.get("product_id")
# #         if pid != product_id and pid in products:
# #             results.append(products[pid])
# #         if len(results) >= top_k:
# #             break

# #     return results



# @app.post("/search")
# def search_products(request: SearchRequest):
#     retriever = get_retriever(k=request.top_k)
#     docs = retriever.invoke(request.query)  # ✅ invoke instead of get_relevant_documents

#     file_path = Path(__file__).parent / "data/products.json"
#     with open(file_path, "r", encoding='utf-8') as f:
#         products = {p["product_id"]: p for p in json.load(f)}

#     results = []
#     for doc in docs:
#         pid = doc.metadata.get("product_id")
#         if pid in products:
#             results.append(products[pid])

#     return results


# @app.get("/recommendations/{product_id}")
# def recommend_products(product_id: str, top_k: int = 5):
#     retriever = get_retriever(k=top_k + 1)  # +1 so we can exclude the same product

#     # Load product details
#     file_path = Path(__file__).parent / "data/products.json"
#     with open(file_path, "r", encoding="utf-8") as f:
#         products = {p["product_id"]: p for p in json.load(f)}

#     if product_id not in products:
#         return {"error": "Product not found"}

#     product = products[product_id]
#     query_text = f"{product['product_name']} {product['about_product']}"

#     # Get similar products
#     docs = retriever.invoke(query_text)

#     results = []
#     for doc in docs:
#         pid = doc.metadata.get("product_id")
#         if pid != product_id and pid in products:  # Exclude the same product
#             results.append(products[pid])
#         if len(results) >= top_k:
#             break

#     return results


# from fastapi import FastAPI
# from pydantic import BaseModel
# from backend.chat_chain import ask_ai
# from backend.retriever import get_retriever
# import json
# from pathlib import Path

# app = FastAPI()

# retriever = None  # Global retriever

# class ChatRequest(BaseModel):
#     query: str

# class SearchRequest(BaseModel):
#     query: str
#     top_k: int = 2

# @app.on_event("startup")
# def load_retriever():
#     global retriever
#     retriever = get_retriever()
#     print("Retriever loaded successfully!")

# @app.get("/")
# def read_root():
#     return {"message": "AI Shopping Assistant Backend is running!"}

# @app.post("/chat")
# def chat(request: ChatRequest):
#     response = ask_ai(request.query)
#     return {
#         "answer": response["result"],
#         "sources": [doc.metadata for doc in response["source_documents"]]
#     }

# @app.get("/products")
# def get_products():
#     file_path = Path(__file__).parent/"data/products.json"
#     with open(file_path, "r", encoding="utf-8") as f:
#         products = json.load(f)
#     return products

# @app.get("/products/{product_id}")
# def get_product_by_id(product_id: str):
#     file_path = Path(__file__).parent/"data/products.json"
#     with open(file_path, "r", encoding="utf-8") as f:
#         products = json.load(f)

#     for product in products:
#         if product["product_id"] == product_id:
#             return product
#     return {"error": "Product not found"}

# @app.post("/search")
# def search_products(query: str, top_k: int = 2):
#     docs = retriever.invoke(query)  # Global retriever ka use
#     file_path = Path(__file__).parent / "data/products.json"
#     with open(file_path, "r", encoding='utf-8') as f:
#         products = {p["product_id"]: p for p in json.load(f)}

#     results = []
#     for doc in docs:
#         pid = doc.metadata.get("product_id")
#         if pid in products:
#             results.append(products[pid])

#     return results

# @app.get("/recommendations/{product_id}")
# def recommend_products(product_id: str, top_k: int = 5):
#     # ✅ global retriever ka clone banane ke bajaye search_kwargs override kar do
#     docs = retriever.vectorstore.as_retriever(
#         search_kwargs={"k": top_k + 1}
#     ).invoke(
#         f"{products[product_id]['product_name']} {products[product_id]['about_product']}"
#     )

#     file_path = Path(__file__).parent / "data/products.json"
#     with open(file_path, "r", encoding="utf-8") as f:
#         products = {p["product_id"]: p for p in json.load(f)}

#     if product_id not in products:
#         return {"error": "Product not found"}

#     results = []
#     for doc in docs:
#         pid = doc.metadata.get("product_id")
#         if pid != product_id and pid in products:
#             results.append(products[pid])
#         if len(results) >= top_k:
#             break
#     return results
# 

from fastapi import FastAPI, Request
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
def search_products(query: str, top_k: int = 2):
    try:
        docs = retriever.invoke(query)
        results = []
        seen = set()
        for doc in docs:
            pid = doc.metadata.get("product_id")
            if pid in products_cache and pid not in seen:
                results.append(products_cache[pid])
                seen.add(pid)
        return success_response("Search results", results)
    except Exception as e:
        logging.error(f"Search failed: {e}")
        return error_response("Search failed")

# -------------------- Recommendations --------------------
@app.get("/recommendations/{product_id}")
def recommend_products(product_id: str, top_k: int = 5):
    if product_id not in products_cache:
        return error_response("Product not found")

    try:
        query_text = f"{products_cache[product_id]['product_name']} {products_cache[product_id]['about_product']}"
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
