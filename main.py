import os
from pathlib import Path

import dotenv

from src.csv_patents import CSVPatents
from src.data_downloading import download_dataset
from src.data_processing import process_and_save


# Загрузка переменных из .env
dotenv.load_dotenv()


# URL датасета Google Patents
URL = (
    "https://patents.google.com/"
    "xhr/query?url=language%3DSPANISH&exp=&download=true"
)


# Директория проекта
BASE_DIR = Path(__file__).parent

# Директория для данных
DATA_DIR = BASE_DIR / "data"

# Имя исходного CSV
SOURCE_FILE_NAME = "gp.csv"


def main():
    print("=== Adeptus Patents ===")

    # ---------------------------------------------------------
    # 1. Скачивание исходного датасета
    # ---------------------------------------------------------

    print("\n[1/3] Загрузка Google Patents dataset...")

    if not download_dataset(
            URL,
            str(DATA_DIR),
            SOURCE_FILE_NAME
    ):
        raise RuntimeError(
            "Не удалось скачать Google Patents dataset"
        )

    # ---------------------------------------------------------
    # 2. Подготовка CSV
    # ---------------------------------------------------------

    print("\n[2/3] Подготовка датасета...")

    process_and_save()

    # ---------------------------------------------------------
    # 3. Парсинг страниц патентов
    # ---------------------------------------------------------

    print("\n[3/3] Парсинг патентов...")

    dataset_path = os.getenv("DATASET_PATH")

    if not dataset_path:
        raise RuntimeError(
            "Переменная DATASET_PATH не указана в .env"
        )

    csv = CSVPatents(dataset_path)

    df = csv.parsed_patents_csv()

    print(f"\nГотово. Обработано патентов: {len(df)}")


if __name__ == "__main__":
    main()