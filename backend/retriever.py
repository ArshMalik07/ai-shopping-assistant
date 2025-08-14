# import os
# from dotenv import load_dotenv
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# # Load .env file to access Gemini API key
# load_dotenv()

# # Path to folder containing FAQ documents
# DATA_PATH = "./data/faq_docs"

# # Step 1: Load all .txt documents from the folder
# def load_documents():
#     documents = []
#     for file in os.listdir(DATA_PATH):
#         if file.endswith(".txt"):
#             path = os.path.join(DATA_PATH, file)
#             loader = TextLoader(path)
#             documents.extend(loader.load())
#     return documents

# # Step 2: Build retriever (chunks + embeddings + FAISS)
# def get_retriever():
#     docs = load_documents()

#     # Split large documents into small chunks
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )
#     chunks = splitter.split_documents(docs)

#     # Get Gemini API key from .env
#     api_key = os.getenv("GEMINI_API_KEY")

#     # Initialize Google Gemini Embeddings model
#     embeddings = GoogleGenerativeAIEmbeddings(
#         model="models/embedding-001",
#         google_api_key=api_key
#     )

#     # Store in FAISS vector DB
#     vectorstore = FAISS.from_documents(chunks, embedding=embeddings)

#     # Return retriever interface for querying
#     return vectorstore.as_retriever()


# backend/retriever.py
# import os
# from dotenv import load_dotenv

# # FAISS vectorstore ko load karne ke liye import
# from langchain_community.vectorstores import FAISS

# # Google Generative AI embeddings import (Gemini ke liye)
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# # Retriever banane ka function
# def get_retriever():
#     """
#     Ye function:
#     1. Google Generative AI ka embeddings model load karta hai
#     2. FAISS vectorstore ko local storage se load karta hai
#     3. Us vectorstore ko retriever me convert karta hai
#     """

#     # Embeddings model initialise karte hain (yaha tumhara Gemini ka embedding model use ho raha hai)
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",
#                                               google_api_key=os.getenv("GEMINI_API_KEY"))

#     # FAISS vectorstore ko local directory se load karo
#     # allow_dangerous_deserialization=True isliye lagaya hai kyunki FAISS pickle use karta hai
#     vectorstore = FAISS.load_local(
#         "backend/vectorstore",
#         embeddings,
#         allow_dangerous_deserialization=True
#     )

#     # Retriever return karo (k=3 matlab top 3 relevant results)
#     return vectorstore.as_retriever(search_kwargs={"k": 3})


# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from pathlib import Path
# import os

# def get_retriever():
#     embeddings = GoogleGenerativeAIEmbeddings(
#         model="models/embedding-001",
#         google_api_key=os.getenv("GEMINI_API_KEY"),  # Apna API key yaha daal
#         task_type="retrieval_query",
#         client=None  # Force sync mode
#     )

#     vectorstore_path = Path(__file__).parent / "vectorstore"
#     vectorstore = FAISS.load_local(
#         folder_path=vectorstore_path,
#         embeddings=embeddings,
#         index_name="index",
#         allow_dangerous_deserialization=True
#     )

#     return vectorstore.as_retriever(search_kwargs={"k": 3})

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
import os

def get_retriever(k=3):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        task_type="retrieval_query",
        client=None 
    )

    vectorstore_path = Path(__file__).parent / "vectorstore"
    vectorstore = FAISS.load_local(
        folder_path=vectorstore_path,
        embeddings=embeddings,
        index_name="index",
        allow_dangerous_deserialization=True
    )

    return vectorstore.as_retriever(search_kwargs={"k": k})
