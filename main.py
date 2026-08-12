import os
from pathlib import Path

import dotenv
from pandas import DataFrame

from src.csv_patents import CSVPatents
from src.data_downloading import download_dataset
from src.data_processing import process_and_save

dotenv.load_dotenv('.env')

csv_file_path = os.getenv('DATASET_PATH')

url = "https://patents.google.com/xhr/query?url=language%3DSPANISH&exp=&download=true"
save_directory = Path(__file__).parent / "data"
file_name = "gp.csv"

# Вызов функции
download_dataset(url, str(save_directory), file_name)
new_csv_file_path = os.getenv('OUT_CSV_PATH')

process_and_save()

csv = CSVPatents(csv_file_path)

df: DataFrame = csv.parsed_patents_csv()

df.to_csv(new_csv_file_path)