import pandas as pd
from catboost import CatBoostRegressor


def dummy_predict(X: pd.DataFrame) -> float:
    """
    Инференс на заглушке
    На вход ожидается однострочный датафрейм
    """
    print("===== Features sent to dummy model =====")
    print(X)
    return X["kilometer"][0] + X["powerPS"][0]


def predict(X: pd.DataFrame) -> float:
    """
    Инференс на полной модели model.cbm
    На вход ожидается однострочный датафрейм
    """
    print("===== Features sent to model =====")
    print(X)
    pass # TODO