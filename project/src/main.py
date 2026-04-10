"""ОСНОВНАЯ ТОЧКА ВХОДА ДЛЯ ПРОЕКТА, ЗАПУСКАЕТ СЕРВИС НА FASTAPI"""
"""Запуск: из project/src uvicorn main:app"""

from fastapi import FastAPI, File, HTTPException
from pydantic import BaseModel, Field
from data.request_transformer import validate_request, request_to_features
from time import perf_counter
from model.inference import dummy_predict


app = FastAPI(
    title="Used car price estimator",
    version="0.1.0",
    description=(
        "HTTP-сервис для оценки стоимости подержанного автомобиля"
    ),
    docs_url="/docs",
    redoc_url=None,
)


class PriceRequest(BaseModel):
    """Признаки, которые подаются в модель"""
    brand: str = Field(..., description="")
    model: str = Field(..., description="")
    dateOfRegistration: str = Field(..., description="Дата регистрации автомобиля в формате DD.MM.YYYY")
    powerPS: int = Field(..., ge=0, description="Мощность двигателя (л. с.)")
    mileage: int = Field(..., ge=0, description="Пробег (км)")
    gearbox: str = Field(..., description="Тип КПП: manual или automatic")
    fuelType: str = Field(..., description="Тип топлива")
    notRepairedDamage: bool = Field(..., ge=0, description="Наличие повреждений")
    vehicleType: str = Field(..., description="Тип кузова")
    dateCrawled: int = Field(..., ge=0, description="Дата загрузки объявления")


class PriceResponse(BaseModel):
    """Ответ модели"""
    price: float = Field(..., description="предсказанная цена автомобиля")
    latency_ms: float = Field(..., ge=0.0, description="Время обработки запроса на сервере, миллисекунды")


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Health-check сервиса."""
    return {
        "status": "ok",
        "service": "used-cars",
        "version": "0.1.0",
    }


@app.post("/price", response_model=PriceResponse, tags=["price"])
def price(req: PriceRequest) -> PriceResponse:
    """
    Эндпоинт, который принимает признаки и возвращает цену автомобиля
    """
    start = perf_counter()

    price = 1000

    latency_ms = (perf_counter() - start) * 1000.0
    return PriceResponse(
        price=price,
        latency_ms=latency_ms
    )