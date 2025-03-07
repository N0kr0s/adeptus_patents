from typing import Generator
import pandas as pd
import dataclasses

from pandas.core.interchange.dataframe_protocol import DataFrame

from parcer import parce
from src.patent import PatentDocument

from config import DATASET_PATH


class CSVPatents:
    def __init__(self, path: str):
        self._path = path  # Path до patents.csv

        # load csv by path

    def rows_filling(self, patent: PatentDocument) -> dict:
        """
        Функция для заполнения строки (словаря) данными из объекта PatentDocument.

        Args:
            patent (PatentDocument): Объект класса PatentDocument, содержащий данные патента.

        Returns:
            dict: Словарь с данными из объекта PatentDocument.
        """
        # Создаем словарь, который будет представлять строку данных
        new_row = {}

        # Используем dataclasses.asdict для преобразования объекта в словарь
        patent_dict = dataclasses.asdict(patent)

        # Заполняем строку данными из объекта
        for index, value in patent_dict.items():
            new_row[index] = value

        return new_row


    def rows(self):
        """Читает старый CSV построчно (или старый датафрейм построчно) и возвращает по одной строке"""
        # yield row # (строка из старого датафрейма)
        df = pd.read_csv(DATASET_PATH)
        for index, row in df.iterrows():
            yield row

    def parsed_patents_csv(self) -> DataFrame:
        # 1. создать новый DataFrame
        columns = [
            "id","title","assignee","inventor/author","priority date","filing/creation date","publication date","grant date","url" "abstract", "images", "classifications", "description",
            "claims", "status", "inventor", "patent_citations_value",
            "cited_value", "priority_applications_value", "apps_claiming_priority_value"
        ]
        df_out = pd.DataFrame(columns=columns)

        # 2. Перебираешь все строки csv файла, который подали в этот класс
        for old_row in self.rows():
            try:
                '''
                # 2.1. Добавить в DataFrame новую строку из старого CSV
                df_out.add(old_row)
                '''

                # 2.2. Запустить парсер для этого патента
                patent: PatentDocument = parce(old_row['url'])

                # 2.3. Заполнить строку новыми данными из объекта парсера
                new_row = old_row
                new_row = self.rows_filling(patent)
                '''
                # 2.4. Сохранить строку в новом DataFrame
                df_out.add(new_row)
                '''
                # 2.4.1 Добавить строку в DataFrame
                df_out = pd.concat([df_out, pd.DataFrame([new_row])], ignore_index=True)

            except Exception as e:
                print(f"Ошибка при обработке строки {old_row.get('url')}: {e}")

        # 3. Вернуть DataFrame
        return df_out

if __name__ == '__main__':
    csv = CSVPatents('str')

    for patent in csv.all(limit=5):
        print(patent)

