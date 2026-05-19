"""ОСНОВНАЯ ТОЧКА ВХОДА ДЛЯ ПРОЕКТА, ЗАПУСКАЕТ СЕРВИС НА FASTAPI"""
"""Запуск: из project/src uvicorn main:app"""

from fastapi import FastAPI, HTTPException
from data.request_transformer import get_incorrect_features, request_to_features
from time import perf_counter
from model.inference import dummy_predict, predict
from utils.request_response_model import PriceRequest, PriceResponse
import logging
import sys
import uuid

logger = logging.getLogger("car_price_service")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)


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
    
    request_id = str(uuid.uuid4())[:8] ## uuid запроса
    logger.info(f"[{request_id}] Request =  {req.model_dump_json()}")

    user_errors = get_incorrect_features(req)
    if len(user_errors) == 0:
        features = request_to_features(req)
        price = predict(features)
    else:
        logger.error(f"[{request_id}] Invalid user input", exc_info=True)
        raise HTTPException(400, f"Введены некорректные значения признаков: {", ".join(user_errors)}")

    latency_ms = (perf_counter() - start) * 1000.0

    response = PriceResponse(
        price=price,
        latency_ms=latency_ms
    )
    logger.info(f"[{request_id}] Response = {response.model_dump_json()}")
    return response


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