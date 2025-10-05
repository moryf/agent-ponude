from core.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from schemas.calculation import Zahtev, FinalniPredlog
from tools.ponude_tools import pronadji_relevantne_primere_iz_arhive

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0,
    verbose=True,
    max_retries=3,
)

tools = [pronadji_relevantne_primere_iz_arhive]

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
    You are an expert in preparing business proposals for clients based on their requests.
    You have access to a tool that allows you to find relevant examples of past proposals from an archive.
    Use this tool to gather information and generate a final proposal that meets the client's needs.
    Ensure that the final proposal is structured according to the 'FinalniPredlog' schema.
    """,
    response_format=FinalniPredlog
)



def predlog_iz_upita(zahtev:Zahtev) -> FinalniPredlog:
    """
    Ova funkcija pokrece LLM da obradi zahtev.
    Prvo se zove alat za pronalazenje relevantnih primera iz arhive,
    a zatim se koristi LLM da se generise finalni predlog u skladu sa
    'FinalniPredlog' schemom.
    """
    print("Pokrecem obradu zahteva...")
    prompt = {"messages": [
        {"role": "system", "content": "You are an expert in preparing business proposals."},
        {"role": "user", "content": f"Klijent ({zahtev.ime}, sa brojem telefona {zahtev.broj_telefona}, email {zahtev.email}) je poslao sledeci zahtev: {zahtev.opis}. Pripremi finalni predlog u skladu sa 'FinalniPredlog' schemom."}
    ]}
    response = agent.invoke(prompt)
    print("Finalni predlog generisan:")
    print(response["structured_response"])
    print("Zavrsena obrada zahteva.")

    return response