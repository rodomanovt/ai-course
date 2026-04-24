import pandas as pd


def dummy_predict(X: pd.DataFrame) -> float:
    """
    Инференс на заглушке
    На вход ожидается однострочный датафрейм
    """
    print("===== Features sent to model =====")
    print(X)
    return X["kilometer"][0] + X["powerPS"][0]