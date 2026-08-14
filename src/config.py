import os
from dotenv import load_dotenv

load_dotenv()


SOURCE_CSV_PATH: str = os.getenv("SOURCE_CSV_PATH")

DATASET_PATH: str = os.getenv("DATASET_PATH")

MAX_ROWS_VALUE: int = int(
    os.getenv("MAX_ROWS_VALUE", "5000")
)

OUT_CSV_PATH: str = os.getenv("OUT_CSV_PATH")

MAX_WORKERS: int = int(
    os.getenv("MAX_WORKERS", "10")
)

SAVE_EVERY: int = int(
    os.getenv("SAVE_EVERY", "1000")
)

REQUEST_TIMEOUT: int = int(
    os.getenv("REQUEST_TIMEOUT", "30")
)

MAX_RETRIES: int = int(
    os.getenv("MAX_RETRIES", "3")
)