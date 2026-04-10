import pandas as pd
import os
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2] # project/
CAT_FEATURES = ["gearbox", "fuelType", "notRepairedDamage", "vehicleType", "model", "brand"]


def get_mapping() -> dict[str: int]:
    """Извлечение маппинга категориальных значений из project/configs/categorial_map.json"""
    mapping_path = os.path.join(BASE_DIR, "configs", "categorial_map.json")
    with open(mapping_path, 'r', encoding='utf-8') as file:
        mapping = json.load(file)
        return mapping


def _make_mapping(df: pd.DataFrame) -> dict[str: int]:
    """Создание маппинга для категориальных значений и сохранение его в project/configs/categorial_map.json"""
    mapping_path = os.path.join(BASE_DIR, "configs", "categorial_map.json")
    mapping = dict()


    for feature in CAT_FEATURES:
        mapping[feature] = {}

        values = df[feature].unique() # значения категориальных признаков
        for i, el in enumerate(values, 0):
            mapping[feature][el] = i
    
    with open(mapping_path, 'w', encoding='utf-8') as file:
        json.dump(mapping, file, indent=4)


def _filter_dataset(df: pd.DataFrame, anomalies_quantile: float = 0.99) -> pd.DataFrame:
    """Фильтрация строк с пропусками и аномальными значениями"""

    # так как размер датасета большой, то уберем все строки, содержащие пропуски хотя бы в одном поле
    df.dropna(inplace=True)

    """
    Удаляем столбцы:
        index - ID записи
        nrOfPictures - константный
        seller, offerType - почти константные
        abtest - флаг, на цену не влияет
        dateCreated - дата создания записи
        name - 233к уникальных значений, для обучения бесполезно
    """

    columns_to_remove = ['index', "nrOfPictures", "seller", "offerType", "abtest", "dateCreated", "name"]
    for col in columns_to_remove:
        df = df.drop(col, axis=1)

    # Убираем экстремальные значения по заданному квантилю в колонках price, yearOfRegistration, powerPS
    columns_to_check = ['price', 'yearOfRegistration', 'powerPS']

    df_filtered = df.copy()
    for col in columns_to_check:
        q_low = df[col].quantile(1-anomalies_quantile)
        q_high = df[col].quantile(anomalies_quantile)
        df_filtered = df_filtered[(df_filtered[col] >= q_low) & (df_filtered[col] <= q_high)]

    df_filtered = df_filtered.reset_index(drop=True)
    _make_mapping(df_filtered)

    return df_filtered



def _make_features_df(df: pd.DataFrame) -> pd.DataFrame:
    """Выделение признаков из данных"""

    # Числовые поля оставляем без изменений
    df_features = df.select_dtypes(include='number')

    # Кодируем категориальные признаки:
    mapping = get_mapping()
    for feature in CAT_FEATURES:
        df_features[feature] = df[feature].map(mapping[feature])

    # Добавим признак monthCrawled, чтобы уловить сезонные колебания цены
    df_features['monthCrawled'] = pd.to_datetime(df['dateCrawled'], errors='coerce').dt.month

    return df_features


def load_and_prepare_dataset(input_filename: str, anomalies_quantile: float = 0.99, save=True) -> pd.DataFrame:
    """Основная функция для загрузки и подготовки датасета
    Сохраняет подготовленные данные в project/data"""
    dataset_dir = os.path.join(BASE_DIR, "data", input_filename)
    df = pd.read_csv(dataset_dir, sep=',', encoding='utf-8')
    df_filtered = _filter_dataset(df, anomalies_quantile=anomalies_quantile)
    df_features = _make_features_df(df_filtered)
    print(f"Датасет подготовлен: {df_features.shape=}")

    if save:
        df_features.to_csv(os.path.join(BASE_DIR, "data", f"{input_filename.replace('.csv', '')}_prepared.csv"))
        print("Датасет сохранен.")

    return df_features


if __name__ == "__main__":
    df = load_and_prepare_dataset("dataset_autos_full.csv", save=True)
    print(df)