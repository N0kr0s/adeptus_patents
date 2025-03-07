import os
from pathlib import Path

import dotenv

from data_downloading import download_dataset

dotenv.load_dotenv('.env') # Загружает переменные окружения

from data_processing import process_excel_and_save

# 1
gp_file_path = os.getenv('SOURCE_CSV_PATH')
csv_file_path = os.getenv('DATASET_PATH')

url = "https://patents.google.com/xhr/query?url=language%3DSPANISH&exp=&download=true"
save_directory = Path(__file__).parent / "data"
file_name = "gp.csv"

# Вызов функции
download_dataset(url, str(save_directory), file_name)
new_csv_file_path = os.getenv('OUT_CSV_PATH')

process_excel_and_save()

'''
# 2
csv = CSVPatents(csv_file_path)

# 3
df: DataFrame = csv.parsed_patents_csv()

# 4 Делай что хочешь (сохраняй, удаляй, еби)
df.to_csv(new_csv_file_path)

'''