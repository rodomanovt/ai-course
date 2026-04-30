"""Подготовка данных и обучение демонстрационной модели CatBoostRegressor
 с сохраненным конфигом на небольшой выборке
 
 Обучение основной модели производится в notebooks/model_experiments.ipynb
 """
from data.data_loader import load_and_prepare_dataset
import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from catboost import CatBoostRegressor, Pool
import json
import os
from data.data_loader import BASE_DIR


RANDOM_STATE = 42
CONFIG_DIR = os.path.join(BASE_DIR, "configs", "model_config.json")
MODEL_DIR = os.path.join(BASE_DIR, "artifacts", "model_mini.cbm")


def set_seed(seed: int = RANDOM_STATE):
    np.random.seed(seed)
    random.seed(seed)


def split_dataset(df: pd.DataFrame, 
                  splits: tuple = (0.7, 0.15, 0.15), 
                  random_state: int = RANDOM_STATE) -> tuple[pd.DataFrame]:
    """
    Разбивает DataFrame на train/val/test
    """
    train_frac, val_frac, test_frac = splits
    
    test_size = test_frac / sum(splits)
    train_val_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
    
    val_size = val_frac / (train_frac + val_frac)
    train_df, val_df = train_test_split(train_val_df, test_size=val_size, random_state=random_state)
    
    return (
        train_df.reset_index(drop=True),
        val_df.reset_index(drop=True),
        test_df.reset_index(drop=True)
    )


def calculate_metrics(y_true: pd.Series, y_pred: np.ndarray, min_price: float = 100) -> dict:
    """
    Вычисляет метрики регрессии.
    min_price: игнорируем автомобили дешевле этой суммы при расчёте MAPE
    """
    
    metrics = {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "r2": r2_score(y_true, y_pred),
    }
    
    # Безопасный MAPE: исключаем очень дешёвые авто
    mask = y_true >= min_price
    if mask.sum() > 0:
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
        metrics["MAPE"] = mape
    else:
        metrics["MAPE"] = np.nan
        
    return metrics


def print_metrics(metrics: dict, model_name: str = "Model"):
    """Красиво выводит метрики в консоль."""
    print(f"\n {model_name}")
    print("─" * 35)
    for name, value in metrics.items():
        print(f"{name:<6} | {value:.2f}")
    print("─" * 35)



def main():
    set_seed(RANDOM_STATE)

    full_df = load_and_prepare_dataset("dataset_autos_mini.csv", save=False)

    train_df, val_df, test_df = split_dataset(full_df, splits=(0.7, 0.15, 0.15))

    TARGET = "price"
    FEATURES = [col for col in train_df.columns if col != TARGET]
    X_train, y_train = train_df[FEATURES], train_df[TARGET]
    X_val, y_val = val_df[FEATURES], val_df[TARGET]
    X_test, y_test = test_df[FEATURES], test_df[TARGET]

    # sanity-check
    print("==== Features ====")
    print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
    print(f"==== Targets ====")
    print(f"Train: {y_train.shape}, Val: {y_val.shape}, Test: {y_test.shape}")

    with open(CONFIG_DIR, 'r', encoding='utf-8') as f:
        config = json.load(f)["params"]
    print(config)

    train_pool = Pool(X_train, y_train)
    val_pool = Pool(X_val, y_val)

    catboost_model = CatBoostRegressor(**config)

    catboost_model.fit(
        train_pool,
        eval_set=val_pool,
    )

    
    test_preds = catboost_model.predict(X_test)
    test_metrics = calculate_metrics(y_test, test_preds)
    print_metrics(test_metrics, "Mini CatBoostRegressor (Test)")

    catboost_model.save_model(MODEL_DIR, format="cbm")
    print(f"Модель сохраненена в {MODEL_DIR}")



if __name__ == "__main__":
    main()