import pandas as pd
import os
from config import *

def process_and_save():
    """
    Обрабатывает данные из датасета и сохраняет первые MAX_ROWS_VALUE записей в файл основного датасета.

    :param file_path_gp: Путь к google_patents-датасету.
    :param file_path_csv: Путь к файлу основного датасета для сохранения результатов.
    """
    try:
        # Чтение Excel-файла, пропуская первую строку
        df = pd.read_csv(SOURCE_CSV_PATH, skiprows=1)
    except Exception as e:
        print(f"Ошибка при чтении google_patents-файла {SOURCE_CSV_PATH}: {e}")
        return

    # Переименование столбцов (если они не читаются корректно)
    df.columns = [
        'id', 'title', 'assignee', 'inventor/author', 'priority date',
        'filing/creation date', 'publication date', 'grant date',
        'result link', 'representative figure link'
    ]

    # Очистка DataFrame от строк с пустыми значениями в столбце 'result link'
    df = df[df['result link'].notna()]

    # Выбор первых MAX_ROWS_VALUE записей
    df_limited = df.head(MAX_ROWS_VALUE)

    # Создание подмножества необходимых столбцов и создание копии
    columns_to_save = [
        'id', 'title', 'assignee', 'inventor/author', 'priority date',
        'filing/creation date', 'publication date', 'grant date', 'result link'
    ]
    df_final = df_limited[columns_to_save].copy()  # Явно создаем копию

    # Переименование столбца 'result link' в 'url'
    df_final = df_final.rename(columns={'result link': 'url'})  # Без inplace=True

    # Сохранение в CSV-файл
    os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)  # Создаем директорию, если она не существует
    df_final.to_csv(DATASET_PATH, index=False)

    print(f"Первые {MAX_ROWS_VALUE} записей успешно сохранены в {DATASET_PATH}")