from retriever import get_retriever

retriever = get_retriever()
query = "What is the return policy for earbuds?"

docs = retriever.get_relevant_documents(query)

for doc in docs:
    print("\n--- Retrieved Chunk ---")
    print(doc.page_content)
