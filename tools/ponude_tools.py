from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import requests

from pydantic import ValidationError

from schemas.calculation import Proizvod, FinalniPredlog

CHROMA_PATH = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

@tool("pronadji_relevantne_primere_iz_arhive")
def pronadji_relevantne_primere_iz_arhive(upit: str) -> str:
    """
    Koristi ovaj alat PRVO i UVEK da pronades najslicnije prethodno radene ponude
    na osnovu korisnickog upita. Ovo ti daje kljucan kontekst i primere od kojih komponenti
    se trazeni proizvod sastoji i kako su se slicni projekti radili u proslosti.
    Ulaz je kompletan tekstualni upit klijenta.
    """
    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function,collection_name="ponude_konstil")
    print("Uspesno povezana baza")
    results = vector_store.similarity_search(upit, k=10)
    if not results:
        return "Nema relevantnih primera u bazi znanja. Moraces da sastavis predlog od nule."
    print("Pronadjeni su primeri iz arhive")
    context = "Pronadeni su sledeci relevantni primeri iz arhive ponuda:\n"
    for i, doc in enumerate(results, 1):
        context += f"--- Primer {i} ---\n{doc.page_content}\n"
    return context

@tool("pretrazi_bazu_proizvoda_sifra")
def pretrazi_bazu_proizvoda_sifra(sifra:str) -> Proizvod:
    """
    Koristi ovaj alat UVEK KAD PRAVIS STAVKE KALKULACIJE da pronadjes proizvod u bazi proizvoda firme Konstil.
    Koristi Ovaj alat nakon sto si koristio pronadji_relevantne_primere_iz_arhive.
    Pokusaj da nadjes sve proizvode koji najvise su ti potrebni za sastavljanke kalulacije.
    Ovi proizvodi se koriste kao Stavke Kalkulacije u ponudi.
    Ulazni parametri su sifra.
    Ako nadjes proizvod, vrati ga kao objekat Proizvod.
    Ako ne nadjes proizvod, vrati None.
    :param naziv: Naziv proizvoda
    :param opis: Opis proizvoda
    :return: Proizvod ili None
    """
    API_BASE_URL = "http://konstil_joilart:konstil2024@localhost:8080/api"

    results = requests.get(f"{API_BASE_URL}/proizvod/{sifra}")

    if results.status_code != 200:
        print(f"Greska prilikom pretrage proizvoda: {results.status_code} - {results.text}")
        return None
    proizvod = results.json()
    print(f"Pronadjen proizvod sa sifrom {sifra}")
    print(proizvod)
    # Ako nema rezultata, vrati None
    if not proizvod:
        return None
    # Uzmi prvi proizvod iz rezultata
    proizvod_data = proizvod
    try:
        proizvod = Proizvod(**proizvod_data)
        return proizvod
    except ValidationError as e:
        print(f"Greska prilikom parsiranja proizvoda: {e}")
        return None


@tool("pretrazi_bazu_proizvoda_naziv_opis")
def pretrazi_bazu_proizvoda_naziv_opis(naziv: str, opis:str) -> Proizvod:
    """
    Koristi ovaj alat da pronadjes proizvod u bazi proizvoda firme Konstil, ukoliko nnisi uspeo da ih nadjes po sifri sa alatom pretrazi_bazu_proizvoda_sifra.
    Pokusaj da nadjes sve proizvode koji najvise su ti potrebni za sastavljanke kalulacije.
    Ovi proizvodi se koriste kao Stavke Kalkulacije u ponudi.
    Ulazni parametri su sifra, naziv i opis proizvoda.
    PRVO probaj da nadjes proizvod po sifri, ako ne uspem onda probaj po nazivu, a ako ni to ne uspe onda probaj po opisu, ili nekoj kombinaciji sva 3.
    Ako nadjes proizvod, vrati ga kao objekat Proizvod.
    Ako ne nadjes proizvod, vrati None.
    :param naziv: Naziv proizvoda
    :param opis: Opis proizvoda
    :return: Proizvod ili None
    """
    API_BASE_URL = "http://konstil_joilart:konstil2024@localhost:8080/api"

    results = requests.get(f"{API_BASE_URL}/proizvod/pretrazi/sifra=/naziv={naziv}/opis={opis}")
    if results.status_code != 200:
        print(f"Greska prilikom pretrage proizvoda: {results.status_code} - {results.text}")
        return None
    proizvodi = results.json()
    print(f"Pronadjeno {len(proizvodi)} proizvoda za naziv={naziv}, opis={opis}.")
     # Ako nema rezultata, vrati None
    if not proizvodi:
        return None
    # Uzmi prvi proizvod iz rezultata
    proizvod_data = proizvodi[0]
    try:
        proizvod = Proizvod(**proizvod_data)
        return proizvod
    except ValidationError as e:
        print(f"Greska prilikom parsiranja proizvoda: {e}")
        return None

def sacuvaj_finalni_predlog(finalni_predlog: FinalniPredlog) -> dict:
    """
    Koristi ovaj alat UVEK kao poslednji korak.
    Nakon sto sastavis kompletan finalni predlog, koristi ovaj alat da ga sacuvas na glavni serve
    :param finalni_predlog: FinalniPredlog objekat koji treba da se cuva na serveru
    :return: dict Ponude sacuvane
    """
    print("Cuva se podatak")
    API_BASE_URL = "http://konstil_joilart:konstil2024@localhost:8080/api"

    results = requests.post(f"{API_BASE_URL}/ponuda/finalniPredlog", finalni_predlog)
    if results.status_code != 200:
        print(f"Greska prilikom pretrage proizvoda: {results.status_code} - {results.text}")
    return None
    ponuda = results.json()
    print(ponuda)
    return ponuda