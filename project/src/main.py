"""ОСНОВНАЯ ТОЧКА ВХОДА ДЛЯ ПРОЕКТА, ЗАПУСКАЕТ СЕРВИС НА FASTAPI"""
"""Запуск: из project/src uvicorn main:app"""

from fastapi import FastAPI, File, HTTPException
from data.request_transformer import validate_request, request_to_features
from time import perf_counter
from model.inference import dummy_predict
from utils.request_response_model import PriceRequest, PriceResponse


app = FastAPI(
    title="Used car price estimator",
    version="0.1.0",
    description=(
        "HTTP-сервис для оценки стоимости подержанного автомобиля"
    ),
    docs_url="/docs",
    redoc_url=None,
)


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
    validate_request(req)

    price = 1000

    latency_ms = (perf_counter() - start) * 1000.0
    return PriceResponse(
        price=price,
        latency_ms=latency_ms
    )