from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_PATH = "../chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def test_chroma_connection():
    try:
        embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function,collection_name="ponude_konstil")
        print("ChromaDB connection successful.")
        return True
    except Exception as e:
        print(f"ChromaDB connection failed: {e}")
        return False

def test_chroma_content():
    try:
        embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vector_store = Chroma(collection_name="ponude_konstil",persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        count = vector_store._collection.count()
        print(f"ChromaDB contains {count} documents.")
        return count
    except Exception as e:
        print(f"Failed to retrieve content from ChromaDB: {e}")
        return -1


def test_similarity_search(query: str):
    try:
        embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vector_store = Chroma(collection_name="ponude_konstil",persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        results = vector_store.similarity_search(query, k=5)
        print(f"Similarity search results for query '{query}':")
        for i, doc in enumerate(results, 1):
            print(f"--- Result {i} ---\n{doc.page_content}\n")
        return results
    except Exception as e:
        print(f"Failed to perform similarity search: {e}")
        return []

if __name__ == "__main__":
    test_chroma_connection()
    test_chroma_content()
    test_similarity_search("Dvokrilna kapija zaluzina")