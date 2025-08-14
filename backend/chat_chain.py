# import os
# from dotenv import load_dotenv
# from langchain.chains import RetrievalQA
# from langchain_google_genai import ChatGoogleGenerativeAI
# from backend.retriever import get_retriever

# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")

# llm = ChatGoogleGenerativeAI(
#     model = "gemini-2.5-flash",
#     temperature=0.3,
#     google_api_key=api_key
# )

# retriever = get_retriever()

# qa_chain = RetrievalQA.from_chain_type(
#     llm = llm,
#     retriever = retriever,
#     return_source_documents=True,
# )

# def ask_ai(query:str) -> str:
#     response = qa_chain.invoke({"query": query})
#     return response["result"]



# backend/chat_chain.py
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini ke chat model ke liye import
from langchain_google_genai import ChatGoogleGenerativeAI

# RetrievalQA chain import (LLM + retriever ko combine karne ke liye)
from langchain.chains import RetrievalQA

# Hamara retriever import
from backend.retriever import get_retriever

# LLM (Gemini Pro) initialise karo
# temperature=0.3 => model thoda creative hoga lekin mostly factual
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# Retriever load karo
retriever = get_retriever()

# RetrievalQA chain banate hain (retriever + LLM)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True  # Ye sources bhi return karega
)

# Function jo query lega aur LLM se answer return karega
def ask_ai(query: str):
    """
    User ka query leta hai, retriever se relevant context nikalta hai,
    LLM ko deta hai, aur final answer return karta hai.
    """
    result = qa_chain({"query": query})
    return result
