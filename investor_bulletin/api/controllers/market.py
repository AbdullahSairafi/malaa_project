from fastapi import APIRouter
from resources.market import market_service

router = APIRouter(prefix="/market-prices")


@router.get("/")
def get_market_data_route():
    return market_service.get_market_data()
