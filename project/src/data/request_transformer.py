from typing import Any
from data.data_loader import get_mapping, make_features_df, CAT_FEATURES, NUMERIC_FEATURES
from utils.request_response_model import PriceRequest
import re
from datetime import datetime
import pandas as pd


def _is_valid_date(date_str: str) -> bool:
    """
    Проверяет, что строка имеет строгий формат DD.MM.YYYY 
    и является существующей календарной датой.
    """
    if not isinstance(date_str, str):
        return False
        
    if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", date_str):
        return False
        
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def get_incorrect_features(req: PriceRequest) -> list[str]:
    """Проверка корректности ввода и вывод признаков с ошибками"""
    errors = []
    mapping = get_mapping()

    brands = mapping["brand"].keys()
    if req.brand not in brands:
        errors.append("brand")
    
    models = mapping["model"].keys()
    if req.model not in models:
        errors.append("model")
    
    if not _is_valid_date(req.dateOfRegistration):
        errors.append("dateOfRegistration")

    if req.powerPS <= 0:
        errors.append("powerPS")

    if req.mileage <= 0:
        errors.append("mileage")

    if req.gearbox not in ("manuell", "automatik"):
        errors.append("gearbox")

    fuel_types = mapping["fuelType"].keys()
    if req.fuelType not in fuel_types:
        errors.append("fuelType")

    vehicle_types = mapping["vehicleType"].keys()
    if req.vehicleType not in vehicle_types:
        errors.append("vehicleType")
    
    if not _is_valid_date(req.dateCrawled):
        errors.append("dateCrawled")
    
    return errors

    


# def request_to_features(req: PriceRequest) -> dict[str: int]:
#     """Преобразует ввод пользователя в признаки для модели
#     На этом этапе предполагается, что ввод корректен"""
#     features = {
#         "gearbox", 
#         "fuelType", 
#         "notRepairedDamage", 
#         "vehicleType", 
#         "model", 
#         "brand"
#         'yearOfRegistration', 'powerPS', 'kilometer', 'monthOfRegistration', 'postalCode', 'monthCrawled'
#     }
def request_to_features(request: PriceRequest) -> pd.DataFrame:
    """Преобразует Pydantic-запрос в DataFrame, готовый для model.predict()"""
    
    # 1. Преобразуем модель в словарь (Pydantic v2)
    data = request.model_dump()
    
    # 2. Парсим дату регистрации -> извлекаем год и месяц
    reg_dt = datetime.strptime(data.pop("dateOfRegistration"), "%d.%m.%Y")
    data["yearOfRegistration"] = reg_dt.year
    data["monthOfRegistration"] = reg_dt.month
    
    # 3. Приводим названия к схеме, на которой обучалась модель
    data["kilometer"] = data.pop("mileage")               # mileage -> kilometer
    print(data["notRepairedDamage"])
    data["notRepairedDamage"] = 1 if data["notRepairedDamage"] else 0 # TODO
    
    # 4. Создаём однострочный DataFrame (dateCrawled остаётся для _make_features_df)
    df_raw = pd.DataFrame([data])
    
    # 5. Применяем вашу существующую логику выделения признаков
    df_features = make_features_df(df_raw)
    
    # 6. Жёстко задаём порядок колонок (sklearn/xgboost требуют строгий порядок)
    expected_cols = NUMERIC_FEATURES + CAT_FEATURES
    # Убираем возможные дубли, сохраняя порядок появления
    expected_cols = list(dict.fromkeys(expected_cols))
    
    return df_features[expected_cols]


if __name__ == '__main__':
    get_incorrect_features()