from typing import Generator
import pandas as pd
import dataclasses

from pandas.core.interchange.dataframe_protocol import DataFrame

from parcer import parse
from src.patent import PatentDocument

from config import DATASET_PATH, OUT_CSV_PATH


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

    def parsed_patents_csv(self) -> DataFrame:
        # 1. Создать новый DataFrame
        columns = [
            "id", "title", "assignee", "inventor/author", "priority date",
            "filing/creation date", "publication date", "grant date", "url", "abstract",
            "images", "classifications", "description", "claims", "status", "inventor",
            "patent_citations_value", "cited_value", "priority_applications_value",
            "apps_claiming_priority_value"
        ]
        rows_list = []

        # 2. Перебираем все строки CSV-файла
        for old_row in self.rows():
            try:
                # 2.1. Запускаем парсер для этого патента
                patent: PatentDocument = parse(old_row['url'])

                # 2.2. Заполняем строку новыми данными
                new_row = self.rows_filling(patent, old_row)
                rows_list.append(new_row)

            except Exception as e:
                print(f"Ошибка при обработке строки {old_row.get('url')}: {e}")

        # 3. Создаем DataFrame из списка строк
        df_out = pd.DataFrame(rows_list, columns=columns)

        # 4. Сохраняем DataFrame в файл
        df_out.to_csv(OUT_CSV_PATH, index=False)
        return df_out


if __name__ == '__main__':
    csv = CSVPatents(DATASET_PATH)
    result_df = csv.parsed_patents_csv()
    print(result_df.head())