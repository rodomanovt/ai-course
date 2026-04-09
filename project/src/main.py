"""ОСНОВНАЯ ТОЧКА ВХОДА ДЛЯ ПРОЕКТА, ЗАПУСКАЕТ СЕРВИС НА FASTAPI"""

from fastapi import FastAPI, File, HTTPException
from pydantic import BaseModel, Field
from data.request_transformer import request_to_features


app = FastAPI(
    title="Used car price estimator",
    version="0.1.0",
    description=(
        "Http-сервис для оценки стоимости подержанного автомобиля"
    ),
    docs_url="/docs",
    redoc_url=None,
)


class PriceRequest(BaseModel):
    """Признаки, которые подаются в модель"""
    yearOfRegistration: int
    powerPS: int
    mileage: int
    monthOfRegistration: int
    gearbox: str
    fuelType: str
    notRepairedDamage: bool
    vehicleType: str
    model: str
    brand: str
    monthCrawled: int


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Простейший health-check сервиса."""
    return {
        "status": "ok",
        "service": "used-cars",
        "version": "0.2.0",
    }