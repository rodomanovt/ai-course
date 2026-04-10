from typing import Any
from data.data_loader import get_mapping
from utils.request_response_model import PriceRequest


def validate_request(req: PriceRequest) -> bool:
    """Проверка введенных данных на корректность"""
    pass



def request_to_features(req: PriceRequest) -> dict[str: int]:
    """Преобразует ввод пользователя в признаки для модели
    На этом этапе предполагается, что ввод корректен"""
    pass


if __name__ == '__main__':
    validate_request()