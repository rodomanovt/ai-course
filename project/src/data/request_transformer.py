from typing import Any
from .data_loader import get_mapping


def validate_request() -> bool:
    """Проверка введенных данных на корректность"""
    pass



def request_to_features(
    brand: str,
    model: str,
    dateOfRegistration: str,
    powerPS: int,
    mileage: int,
    gearbox: str,
    fuelType: str,
    notRepairedDamage: bool,
    vehicleType: str,
    dateCrawled: str,
) -> dict[str: int]:
    """Преобразует ввод пользователя в признаки для модели
    На этом этапе предполагается, что ввод корректен"""
    pass


if __name__ == '__main__':
    print(get_mapping())