from pydantic import BaseModel, Field


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