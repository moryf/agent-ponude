import json

from langgraph.prebuilt import create_react_agent

from core.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from schemas.calculation import Zahtev, FinalniPredlog
from tools.ponude_tools import pronadji_relevantne_primere_iz_arhive, pretrazi_bazu_proizvoda_sifra, pretrazi_bazu_proizvoda_naziv_opis, sacuvaj_finalni_predlog
from langchain_core.messages import  HumanMessage

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0,
    verbose=True,
)

agent = create_react_agent(
    model=llm,
    tools=[pronadji_relevantne_primere_iz_arhive, pretrazi_bazu_proizvoda_sifra, pretrazi_bazu_proizvoda_naziv_opis],
    response_format=FinalniPredlog,
    prompt="""
    Ti si expert za davanje ponuda za ograde kapije, nadstresnice i druge metalne konstrukcije za firmu Joilart Konstil d.o.o. iz Srbije.
    Na osnovu upita klijenta, tvoj zadatak je da sastavis detaljan predlog ponude i da ga sacuvas na serveru, koji ukljucuje:
    - Opis trazenog proizvoda
    - Specifikacije materijala
    - Dimenzije
    - Procenu troskova
    UVEK KORISTI alat pronadji_relevantne_primere_iz_arhive da pronadjes najslicnije prethodno radene ponude na osnovu korisnickog upita.
    Ovo ti daje kljucan kontekst i primere od kojih komponenti se trazeni proizvod sastoji i kako su se slicni projekti radili u proslosti.
    Nakon sto dobijes rezultate iz alata pronadji_relevantne_primere_iz_arhive, UVEK KORISTI alat pretrazi_bazu_proizvoda_sifra da pronadjes proizvode koji se koriste u kalkulaciji u bazi proizvoda firme Konstil.
    Ukoliko ne uspes da nadjes proizvod po sifri onda koristi alat pretrazi_bazu_proizvoda_naziv_opis.
    Koristi ove alate da nadjes sve proizvode koji su ti potrebni kao stavke kalkulacije
    Ako alat vrati "Nema relevantnih primera u bazi znanja. Moraces da sastavis predlog od nule.", onda moras da sastavis ponudu od nule.
    UVEK se trudi da ponuda bude sto detaljnija i specificnija.
    Obavezno obracunaj ukupnu cenu po formuli:
    Ukupna cena = Materijal + (izradaPoKg * Ukupna masa + montazaPoKg * Ukupna masa + cinkovanjePoKg * Ukupna masa + parbanjePoM2 * Povrsina) * stepenSigurnosti
    """
)


def predlog_iz_upita(zahtev: Zahtev):
    """
    Prima upit klijenta i vraca generisani predlog ponude.
    """
    upit = f"""
    Klijent: Ime: {zahtev.ime}, Email: {zahtev.email}, Telefon: {zahtev.broj_telefona}.
    Opis zahteva: {zahtev.opis}.
    """
    print("User query:", upit)
    input = {"messages": [HumanMessage(content=upit)]}

    response = agent.invoke(input)

    structured_response = response["structured_response"]

    ponuda = sacuvaj_finalni_predlog(structured_response)

    return ponuda

