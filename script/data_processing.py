import pandas as pd
import os

def process_excel_and_save(file_path_gp, file_path_csv):
    """
    Обрабатывает данные из датасета и сохраняет первые 5000 записей в файл основного датасета.

    file_path_gp: Путь к google_patents-датасету.
    file_path_csv: Путь к файлу основного датасета для сохранения результатов.
    """
    try:
        # Чтение Excel-файла, пропуская первую строку
        df = pd.read_csv(file_path_gp, skiprows=1)
    except Exception as e:
        print(f"Ошибка при чтении google_patents-файла {file_path_gp}: {e}")
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

    # Создание подмножества необходимых столбцов и создание копии
    columns_to_save = [
        'id', 'title', 'assignee', 'inventor/author', 'priority date',
        'filing/creation date', 'publication date', 'grant date', 'result link'
    ]
    df_final = df_limited[columns_to_save].copy()  # Явно создаем копию

    # Переименование столбца 'result link' в 'url'
    df_final = df_final.rename(columns={'result link': 'url'})  # Без inplace=True

    # Сохранение в CSV-файл
    os.makedirs(os.path.dirname(file_path_csv), exist_ok=True)  # Создаем директорию, если она не существует
    df_final.to_csv(file_path_csv, index=False)

    print(f"Первые 5000 записей успешно сохранены в {file_path_csv}")