"""ОСНОВНАЯ ТОЧКА ВХОДА ДЛЯ ПРОЕКТА, ЗАПУСКАЕТ СЕРВИС НА FASTAPI"""
"""Запуск: из project/src uvicorn main:app"""

from fastapi import FastAPI, File, HTTPException
from data.request_transformer import get_incorrect_features, request_to_features
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
    
    user_errors = get_incorrect_features(req)
    if len(user_errors) == 0:
        features = request_to_features(req)
        print(features)
        price = 1000
    else:
        raise HTTPException(400, f"Введены некорректные значения признаков: {", ".join(user_errors)}")

    latency_ms = (perf_counter() - start) * 1000.0
    return PriceResponse(
        price=price,
        latency_ms=latency_ms
    )


"""Пример корректного запроса

{
  "brand": "kia",
  "model": "rio",
  "dateOfRegistration": "01.04.2016",
  "powerPS": 144,
  "mileage": 144000,
  "gearbox": "manuell",
  "fuelType": "benzin",
  "notRepairedDamage": true,
  "vehicleType": "suv",
  "dateCrawled": "06.05.2024"
}

"""