from core.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from schemas.calculation import Zahtev, FinalniPredlog


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0,
)

llm = llm.with_structured_output(FinalniPredlog)

prompt = ChatPromptTemplate.from_messages([
    ("system", """Ti si ekspertni komercijalista u firmi Joilart Konstil.
    Tvoj zadatak je da na osnovu upita klijenta kreiras kompletan i tacan predlog kalkulacije u JSON formatu koji odgovara 'FinalniPredlog' schemi.
    Tvoj finalni odgovor MORA biti ISKLJUcIVO taj JSON objekat.
    Nemoj pisati nikakav dodatni tekst pre ili posle JSON-a.
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