from fastapi import APIRouter
from schemas.calculation import Zahtev, FinalniPredlog
from service.calculation_service import predlog_iz_upita

router = APIRouter()

@router.post("/generate-proposal", response_model=FinalniPredlog)
def generate_proposal_endpoint(zahtev: Zahtev):
    """
    Prima upit klijenta i poziva servisni sloj da obradi zahtev.
    """
    return predlog_iz_upita(zahtev)

