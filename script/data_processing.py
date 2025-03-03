import pandas as pd
import os

def process_excel_and_save(file_path_excel, file_path_csv):
    """
    Обрабатывает данные из Excel-файла и сохраняет первые 5000 записей в CSV-файл.

    :param file_path_excel: Путь к Excel-файлу с данными.
    :param file_path_csv: Путь к CSV-файлу для сохранения результатов.
    """
    try:
        # Чтение Excel-файла, пропуская первую строку
        df = pd.read_excel(file_path_excel, skiprows=1)
    except Exception as e:
        print(f"Ошибка при чтении Excel-файла {file_path_excel}: {e}")
        return

    # Переименование столбцов (если они не читаются корректно)
    df.columns = [
        'id', 'title', 'assignee', 'inventor/author', 'priority date',
        'filing/creation date', 'publication date', 'grant date',
        'result link', 'representative figure link'
    ]

    # Очистка DataFrame от строк с пустыми значениями в столбце 'result link'
    df = df[df['result link'].notna()]

    # Выбор первых 5000 записей
    df_limited = df.head(5000)

    # Создание подмножества необходимых столбцов
    columns_to_save = [
        'id', 'title', 'assignee', 'inventor/author', 'priority date',
        'filing/creation date', 'publication date', 'grant date', 'result link'
    ]
    df_final = df_limited[columns_to_save]

    # Переименование столбца 'result link' в 'url'
    df_final.rename(columns={'result link': 'url'}, inplace=True)

    # Сохранение в CSV-файл
    os.makedirs(os.path.dirname(file_path_csv), exist_ok=True)  # Создаем директорию, если она не существует
    df_final.to_csv(file_path_csv, index=False)

    print(f"Первые 5000 записей успешно сохранены в {file_path_csv}")