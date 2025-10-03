from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
import requests
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

API_BASE_URL = "http://konstil_joilart:konstil2024@localhost:8080/api"
OFFERS_ENDPOINT = "/ponuda/sve/dto"
CHROMA_PATH = "chroma_db"

def get_all_offers_from_api():
    """
    Povlaci sve ponude iz Spring Boot aplikacije.
    """
    print("Povlacenje ponuda sa servera")
    try:
        response = requests.get(f"{API_BASE_URL}{OFFERS_ENDPOINT}")
        response.raise_for_status()
        offers = response.json()
        print(f"Uspecno povuceno {len(offers)} ponuda.")
        return offers
    except requests.exceptions.RequestException as e:
        print(f"Grecka prilikom povlacenja ponuda: {e}")
        return []

def create_document_from_offer(ponuda_data):
    """
    Pretvara kompleksni JSON jedne ponude u jedan smislen tekstualni dokument.
    :param ponuda_data: Podatak o ponudi iz API-ja
    :return: tekstualni dokument
    """
    ponuda = ponuda_data.get("ponuda", {})
    proizvodi_ponude = ponuda_data.get("proizvodPonudaList", [])

    document_text = f"Opis ponude: {ponuda.get('opis', 'Nema opisa')}.\n"
    document_text += f"Status ponude: {ponuda.get('status', 'Nepoznat')}.\n"
    document_text += "Sadrzaj ponude:\n"

    for proizvod_ponuda in proizvodi_ponude:
        proizvod_naziv = proizvod_ponuda.get('naziv', 'Nepoznat proizvod')
        document_text += f"- Proizvod: {proizvod_naziv}\n"
        proizvod_tip = proizvod_ponuda.get('tipProizvodaPonuda', {})
        proizvod_tip_naziv = proizvod_tip.get('naziv', 'Nepoznat tip proizvoda')
        document_text += f"  Tip proizvoda: {proizvod_tip_naziv}\n"

        kalkulacije = proizvod_ponuda.get('kalkulacijaList', [])
        for kalkulacija in kalkulacije:
            naziv_kalkulacije = kalkulacija.get('naziv', 'Nepoznat naziv kalkulacije')
            document_text += f"  - Kalkulacija: {naziv_kalkulacije}\n"
            cinkovanje = kalkulacija.get('cinkovanje', False)
            farbanje = kalkulacija.get('farbanje', False)
            montaza = kalkulacija.get('montaza', False)
            izrada = kalkulacija.get('izrada', False)
            document_text += f"    Cinkovanje: {'Da' if cinkovanje else 'Ne'}, Farbanje: {'Da' if farbanje else 'Ne'}, Montaza: {'Da' if montaza else 'Ne'}, Izrada: {'Da' if izrada else 'Ne'}\n"
            materijal_po_kg = kalkulacija.get('materijalPoKg', 0)
            cinkovanje_po_kg = kalkulacija.get('cinkovanjePoKg', 0)
            farbanje_po_m2 = kalkulacija.get('farbanjePoM2', 0)
            montaza_po_kg = kalkulacija.get('montazaPoKg', 0)
            izrada_po_kg = kalkulacija.get('izradaPoKg', 0)
            rezijski_troskovi_stepen = kalkulacija.get('rezijskiTroskoviStepen', 0)
            stepen_sigurnosti = kalkulacija.get('stepenSigurnosti', 0)
            koriscenje_cene = kalkulacija.get('koriscenjeCene', 'Nepoznat tip cena')
            ukupno_bez_pdv = kalkulacija.get('ukupnoBezPdv', 0)
            ukupno_sa_pdv = kalkulacija.get('ukupnoSaPdv', 0)
            document_text += f"    Cene - Materijal/kg: {materijal_po_kg}, Cinkovanje/kg: {cinkovanje_po_kg}, Farbanje/m2: {farbanje_po_m2}, Montaza/kg: {montaza_po_kg}, Izrada/kg: {izrada_po_kg}, Rezijski troskovi stepen: {rezijski_troskovi_stepen}, Stepen sigurnosti: {stepen_sigurnosti}, Koriscenje cene: {koriscenje_cene}\n"
            document_text += f"    Ukupno bez PDV: {ukupno_bez_pdv}, Ukupno sa PDV: {ukupno_sa_pdv}\n"
            stavke = kalkulacija.get('stavkaKalkulacijeList', [])
            if stavke:
                document_text += "    - Korisceni materijali:\n"
                for stavka in stavke:
                    proizvod_stavke = stavka.get('proizvod', {})
                    sifra = proizvod_stavke.get('sifra', '?')
                    naziv = proizvod_stavke.get('naziv', '?')
                    opis_materijala = proizvod_stavke.get('opis', '')
                    jedinica_mere = proizvod_stavke.get('jedinicaMere', 'kom')
                    document_text += f"    - {naziv} ({opis_materijala} , jedinica mere: {jedinica_mere}) [sifra: {sifra}] \n"
                    kolicina_komada = stavka.get('kolicinaKomada', 0)
                    duzina_komada = stavka.get('duzinaKomada', None)
                    nacin_racunanja_duzine_komada = stavka.get('nacinRacunanjaDuzineKomada', 'N/A')
                    referentna_duzina = stavka.get('referentnaDuzina', 'N/A')
                    razlika_duzine = stavka.get('razlikaDuzine', 'N/A')
                    duzina_komada = stavka.get('duzinaKomada', 'N/A')
                    nacin_racunanja_komada = stavka.get('nacinRacunanjaKomada', 'N/A')
                    razmak = stavka.get('razmak', 'N/A')
                    multiplikator = stavka.get('multiplikator', 'N/A')
                    rucni_dodatak = stavka.get('rucniDodatak', 'N/A')
                    kolicina = stavka.get('kolicina', 'N/A')
                    cinkovanje = stavka.get('cinkovanje', False)
                    farbanje = stavka.get('farbanje', False)
                    montaza = stavka.get('montaza', False)
                    izrada = stavka.get('izrada', False)
                    cena = stavka.get('cena', 'N/A')
                    document_text += f"      Kolicina komada: {kolicina_komada}, Nacin racunanja komada: {nacin_racunanja_komada}, Razmak: {razmak}, Multiplikator: {multiplikator}, Rucni dodatak: {rucni_dodatak}\n"
                    document_text += f"      Nacin racunanja duzine komada: {nacin_racunanja_duzine_komada}, Referentna duzina: {referentna_duzina}, Razlika duzine: {razlika_duzine}, Duzina komada: {duzina_komada}\n"
                    document_text += f"      Ukupna kolicina: {kolicina}, Cinkovanje: {cinkovanje}, Farbanje: {farbanje}, Montaza: {montaza}, Izrada: {izrada}, Cena: {cena}\n"
    print(document_text)
    return document_text.strip()

def main():
    sve_ponude = get_all_offers_from_api()
    if not sve_ponude:
        print("Nema podataka za obradu")
        return
    dokumenti = [create_document_from_offer(ponuda) for ponuda in sve_ponude]
    print(f"Ukupno kreirano {len(dokumenti)} dokumenata za vektorizaciju.")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    chroma_db = Chroma(persist_directory=CHROMA_PATH,embedding_function=embeddings, collection_name="ponude_konstil")
    chroma_db.add_texts(dokumenti)
    print("Dokumenti su uspesno dodati u Chroma vektorsku bazu.")
    print("Chroma vektorska baza je sacuvana na disk.")
    print(f"Vektorska baza je kreirana i sacuvana u '{CHROMA_PATH}'.")
    print(f"Sacuvano {chroma_db._collection.count()} vektora u kolekciji '{chroma_db._collection.name}'.")

if __name__ == "__main__":
    main()

