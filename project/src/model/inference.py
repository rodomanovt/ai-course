import pandas as pd
from catboost import CatBoostRegressor
from data.data_loader import BASE_DIR
import os


MODEL_DIR = os.path.join(BASE_DIR, "artifacts", "model.cbm")
model = CatBoostRegressor()
model.load_model(MODEL_DIR)


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
    
    expected_cols = model.feature_names_
    X = X.reindex(columns=expected_cols)
    
    prediction = float(model.predict(X)[0])
    print(f"===== Prediction: {prediction} =====")
    
    return prediction