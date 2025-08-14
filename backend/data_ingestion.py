import json
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")


DATA_PATH = "data/products.json"
VECTORESTORE_PATH = "vectorestore"


def load_product_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        products = json.load(f)

    docs = []

    for product in products:
        content = (
            f"Product Name: {product['product_name']}\n"
            f"Category: {product['category']}\n"
            f"Discounted Price: {product['discounted_price']}\n"
            f"Actual Price: {product['actual_price']}\n"
            f"Discount Percentage: {product['discount_percentage']}\n"
            f"Rating: {product['rating']} ({product['rating_count']} votes)\n"
            f"About: {product['about_product']}\n"
            f"Product Link: {product['product_link']}\n"
        )

        docs.append(
            Document(
                page_content=content,
                metadata={"product_id": product["product_id"]}
            )
        )

    return docs


def create_vectorstore():
    docs = load_product_data()


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = text_splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    vectorstore.save_local(VECTORESTORE_PATH)

    print(f"Vector store created and saved at {VECTORESTORE_PATH}")


if __name__ == "__main__":
    create_vectorstore()