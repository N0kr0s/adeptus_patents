from typing import Generator
import pandas as pd
import dataclasses

from src.parser import parse
from src.patent import PatentDocument
from src.config import DATASET_PATH, OUT_CSV_PATH

class CSVPatents:
    def __init__(self, path: str):
        self._path = path  # Path до patents.csv

    def rows_filling(self, patent: PatentDocument, old_row: dict) -> dict:
        """
        Объединяет данные из old_row и PatentDocument.
        """
        patent_dict = dataclasses.asdict(patent)
        return {**old_row, **patent_dict}

    def rows(self):
        """Читает старый CSV построчно и возвращает по одной строке."""
        df = pd.read_csv(self._path)
        for _, row in df.iterrows():
            yield row.to_dict()

    def parsed_patents_csv(self) -> pd.DataFrame:
        # 1. Создание нового DataFrame
        columns = [
            "id", "title", "assignee", "inventor/author", "priority date",
            "filing/creation date", "publication date", "grant date", "url", "abstract",
            "images", "classifications", "description", "claims", "status", "inventor",
            "patent_citation_number", "cited_number", "priority_applications_number",
        ]
        rows_list = []

        # 2. Перебор всех строки CSV-файла
        for old_row in self.rows():
            try:
                # 2.1. Запуск парсер для этого патента
                patent: PatentDocument = parse(old_row['url'])

                # 2.2. Заполнение строк новыми данными
                new_row = self.rows_filling(patent, old_row)
                rows_list.append(new_row)

            except Exception as e:
                print(f"Ошибка при обработке строки {old_row.get('url')}: {e}")

        # 3. Сохдание DataFrame из списка строк
        df_out = pd.DataFrame(rows_list, columns=columns)

        # 4. Сохранение DataFrame в файл
        df_out.to_csv(OUT_CSV_PATH, index=False)
        return df_out


if __name__ == '__main__':
    csv = CSVPatents(DATASET_PATH)
    result_df = csv.parsed_patents_csv()
    print(result_df.head())