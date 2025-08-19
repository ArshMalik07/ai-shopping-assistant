# backend/rebuild_vectorstore.py
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document

# Load env vars
load_dotenv()

# Paths
DATA_FILE = Path(__file__).parent / "data/products.json"
VECTORSTORE_PATH = Path(__file__).parent / "vectorstore"
INDEX_NAME = "index"

def _normalize_value(value):
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return ", ".join([_normalize_value(v) for v in value if v is not None])
    if isinstance(value, dict):
        parts = []
        for k, v in value.items():
            if v is None:
                continue
            parts.append(f"{k}: {_normalize_value(v)}")
        return "; ".join(parts)
    return str(value)

def _price_bucket(raw_price):
    try:
        # Strip non-digits (e.g., currency) then parse
        cleaned = ''.join(ch for ch in str(raw_price) if ch.isdigit() or ch == '.')
        price = float(cleaned) if cleaned else 0.0
    except Exception:
        price = 0.0
    # Simple buckets (tune thresholds per catalog)
    if price <= 1000:
        return "budget"
    if price <= 5000:
        return "mid-range"
    return "premium"

def _compose_doc_text(product: dict) -> str:
    name = product.get("product_name") or product.get("name") or ""
    desc = product.get("about_product") or product.get("description") or ""
    category = product.get("category") or ""
    brand = product.get("brand") or product.get("manufacturer") or ""
    specs = _normalize_value(product.get("specs"))
    features = _normalize_value(product.get("features"))
    tags = _normalize_value(product.get("tags"))
    rating = _normalize_value(product.get("rating"))
    price = product.get("price")
    bucket = _price_bucket(price)

    parts = []
    if name: parts.append(f"Name: {name}.")
    if desc: parts.append(f"Description: {desc}.")
    if category: parts.append(f"Category: {category}.")
    if brand: parts.append(f"Brand: {brand}.")
    if specs: parts.append(f"Key specs: {specs}.")
    if features: parts.append(f"Features: {features}.")
    if tags: parts.append(f"Tags: {tags}.")
    if rating: parts.append(f"Rating: {rating}.")
    if price is not None: parts.append(f"Price: {price} ({bucket}).")

    # Fallback minimal content
    if not parts:
        parts.append(str(product))
    return " ".join(parts)

def rebuild_vectorstore():
    # 1️⃣ Load products.json
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    # 2️⃣ Convert to LangChain Document format (enriched content)
    docs = []
    for product in products:
        text = _compose_doc_text(product)
        metadata = {"product_id": product.get("product_id") or product.get("id")}
        if not metadata["product_id"]:
            # Skip items without an identifier
            continue
        docs.append(Document(page_content=text, metadata=metadata))

    # 3️⃣ Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    # 4️⃣ Create FAISS index
    vectorstore = FAISS.from_documents(docs, embedding=embeddings)

    # Ensure folder exists
    VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)

    # 5️⃣ Save FAISS index locally
    vectorstore.save_local(folder_path=VECTORSTORE_PATH, index_name=INDEX_NAME)
    print(f"✅ Vectorstore rebuilt successfully with {len(docs)} products.")

if __name__ == "__main__":
    rebuild_vectorstore()
