"""Подготовка данных и обучение модели с сохраненным конфигом на небольшой демонстрационной выборке"""
from data.data_loader import load_and_prepare_dataset


def main():
    df_name_mini = "dataset_autos_mini.csv"
    df = load_and_prepare_dataset()


if __name__ == "__main__":
    main()