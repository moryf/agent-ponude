from core.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from schemas.calculation import Zahtev, FinalniPredlog


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0,
    verbose=True
)

llm = llm.with_structured_output(FinalniPredlog)

prompt = ChatPromptTemplate.from_messages([
    ("system", """Ti si ekspertni komercijalista u firmi Joilart Konstil.
    Tvoj zadatak je da na osnovu upita klijenta kreiras kompletan i tacan predlog kalkulacije u JSON formatu koji odgovara 'FinalniPredlog' schemi.
    Tvoj finalni odgovor MORA biti ISKLJUcIVO taj JSON objekat.
    Nemoj pisati nikakav dodatni tekst pre ili posle JSON-a.
    Finalni predlog mora sadrzati sledece:
    1. Podatke o klijentu (ime, telefon, email).
    2. Naziv ponude (npr. "Ponuda za kapiju i ogradu").
    3. Listu proizvoda u ponudi, gde svaki proizvod sadrzi:
       - Naziv proizvoda (npr. "Kapija", "Ograda").
       - Tip proizvoda (npr. "Kapija", "Ograda", "Gelender").
       - Ukupno metara i komada.
       - Dimenzije po komadu (duzina, visina, dubina).
       - Detaljnu kalkulaciju troskova, ukljucujuci:
         - Stavke kalkulacije sa nazivom, kolicinom, jedinicom mere, cenom po jedinici, ukupnom cenom, i tipom troska (materijal, rad, usluga).
         - Troskove po kg/m2 za materijal, cinkovanje, farbanje, montazu, izradu.
         - Rezijske troskove i stepen sigurnosti.
         - Ukupno bez PDV i ukupno sa PDV.
    Koristi sledece cene:
    - Materijal po kg: 115.0
    - Cinkovanje po kg: 115.0
    - Farbanje po m2: 960.0
    - Montaza po kg: 200.0
    - Izrada po kg: 115.0
    - Rezijski troskovi: 1.0
    - Stepen sigurnosti: 1.5
    Koristi veleprodajne cene.
    Ako neki podatak nije naveden u upitu, proceni realnu vrednost.
    """),
    ("human", "{input}"),
])

def predlog_iz_upita(zahtev:Zahtev) -> FinalniPredlog:
    """
    Ova funkcija pokrece LLM da obradi zahtev.
    """
    print(f"--- Pokretanje LLM sa upitom: {zahtev.opis} ---")

    full_input = (
        f"Podaci o klijentu: Ime: {zahtev.ime}, Telefon: {zahtev.broj_telefona}, Email: {zahtev.email}. "
        f"Tekst upita: {zahtev.opis}"
    )

    odgovor = llm.invoke(prompt.format_messages(input=full_input))
    print(f"--- LLM Odgovor: {odgovor} ---")

    return odgovor