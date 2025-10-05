from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = "../chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

@tool
def pronadji_relevantne_primere_iz_arhive(upit: str) -> str:
    """
    Koristi ovaj alat PRVO i UVEK da pronades najslicnije prethodno radene ponude
    na osnovu korisnickog upita. Ovo ti daje kljucan kontekst i primere od kojih komponenti
    se trazeni proizvod sastoji i kako su se slicni projekti radili u proslosti.
    Ulaz je kompletan tekstualni upit klijenta.
    """
    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    results = vector_store.similarity_search(upit, k=5)
    if not results:
        return "Nema relevantnih primera u bazi znanja. Moraces da sastavis predlog od nule."
    context = "Pronadeni su sledeci relevantni primeri iz arhive ponuda:\n"
    for i, doc in enumerate(results, 1):
        context += f"--- Primer {i} ---\n{doc.page_content}\n"
    print(context)
    return context
