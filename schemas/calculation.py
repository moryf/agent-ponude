from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


#Struktura Zahteva
class Zahtev(BaseModel):
    """
    Schema za zahtev koji sadrži upit klijenta.
    """
    ime: str
    broj_telefona: str
    email: Optional[EmailStr] = None
    opis: str
    timestamp: datetime = Field(default_factory=datetime.now)

#Enum za jedinice mere
class JedinicaMere(str, Enum):
    KOMAD = "KOMAD"
    METAR = "METAR"

#Struktura Proizvoda
class Proizvod(BaseModel):
    """
    Schema za jedan proizvod koji je deo ponude.
    """
    sifra: str
    naziv: str
    opis: Optional[str] = None
    jedinicaMere: JedinicaMere
    masa: float
    specificnaPovrsina: float
    cenaA: float
    veleprodajnaCena: float


# Nacin Racunanja Komada enum
class NacinRacunanjaKomada(str, Enum):
    KOMAD = "KOMAD"
    PO_DUZNOM_METRU = "PO_DUZNOM_METRU"
    PO_VISINSKOM_METRU  = "PO_VISINSKOM_METRU"
    PO_DUBINSKOM_METRU = "PO_DUBINSKOM_METRU"

# Nacin racunanja duzine komada enum
class NacinRacunanjaDuzineKomada(str, Enum):
    UPISANO = "UPISANO"
    DUZINA = "DUZINA"
    VISINA = "VISINA"
    DUBINA = "DUBINA"

# Struktura Stavke Kalkulacije
class StavkaKalkulacije(BaseModel):
    """
    Schema za jednu stavku materijala unutar kalkulacije.
    """
    proizvod: Proizvod

    nacinRacunanjaKomada: NacinRacunanjaKomada = NacinRacunanjaKomada.KOMAD
    razmak: float = 0
    multiplikator: float = 0
    rucniDodatak: float = 0
    kolicina_komada: float = 0

    nacinRacunanjaDuzineKomada: NacinRacunanjaDuzineKomada = NacinRacunanjaDuzineKomada.UPISANO
    referentnaDuzina: float = 0
    razlikaDuzine: float = 0
    duzinaKomada: float = 0

    kolicina: float
    cinkovanje: bool
    farbanje: bool
    montaza: bool
    izrada: bool
    cena: float

#Koriscenje cene enum
class KoriscenjeCene(str, Enum):
    CENA_A = "CENA_A"
    VELEPRODAJNA_CENA = "VELEPRODAJNA_CENA"

# Struktura Kalkulacije
class Kalkulacija(BaseModel):
    """
    Schema za jednu kompletan kalkulaciju za jedan finalni proizvod.
    """
    datumOtvaranja: datetime = Field(default_factory=datetime.now)
    poslednjiDatumIzmene: datetime = Field(default_factory=datetime.now)
    naziv: str
    cinkovanje: bool
    farbanje: bool
    montaza: bool
    izrada: bool
    stavkaKalkulacijeList: List[StavkaKalkulacije] = []
    materijalPoKg: float
    cinkovanjePoKg: float
    farbanjePoM2: float
    montazaPoKg: float
    izradaPoKg: float
    rezijskiTroskoviStepen: float
    stepenSigurnosti: float
    koriscenjeCene: KoriscenjeCene = KoriscenjeCene.VELEPRODAJNA_CENA

    ukupnoBezPdv: float
    ukupnoSaPdv: float

#TipProizvodaPonuda struktura
class TipProizvodaPonuda(BaseModel):
    """
    Schema za tip proizvoda iz baze (npr. "Kapija", "Ograda", "Gelender").
    """
    naziv: str

# Proizvod ponude struktura
class ProizvodPonude(BaseModel):
    """
    Schema za jedan finalni proizvod koji je deo ponude (npr. "Kapija", "Ograda").
    """
    naziv: str
    tipProizvodaPonuda: TipProizvodaPonuda
    ukupnoMetara: float
    ukupnoKomada: float
    duzinaPoKomadu: float
    visinaPoKomadu: float
    dubinaPoKomadu: float
    kalkulacijaList: List[Kalkulacija] = []

# Glavna, krovna šema za kompletan odgovor koji agent generiše.
class FinalniPredlog(BaseModel):
    """
    Glavna, krovna šema za kompletan odgovor koji agent generiše.
    """
    kupac_ime_prezime: str
    kupac_adresa: Optional[str] = None
    kupac_broj_telefona: str
    kupac_email: Optional[EmailStr] = None
    ponuda_naziv: str
    ponuda_opis: str
    proizvodi_ponude: List[ProizvodPonude] = []

