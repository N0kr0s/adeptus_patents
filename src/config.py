import os
from dotenv import load_dotenv
load_dotenv()

SOURCE_CSV_PATH: str = os.getenv('SOURCE_CSV_PATH')

DATASET_PATH: str = os.getenv('DATASET_PATH')

MAX_ROWS_VALUE: int = int(os.getenv('MAX_ROWS_VALUE'))

OUT_CSV_PATH: str = os.getenv('OUT_CSV_PATH')
