from typing import Generator

from pandas.core.interchange.dataframe_protocol import DataFrame

from parcer import parce
from src.patent import PatentDocument


class CSVPatents:
    def __init__(self, path: str):
        self._path = path  # Path до patents.csv

        # load csv by path

    def rows(self):
        """Читает старый CSV построчно (или старый датафрейм построчно) и возвращает по одной строке"""
        # yield row # (строка из старого датафрейма)
        ...
    def all(self, limit: int = 100) -> Generator[PatentDocument]:

        for number, url in enumerate(self.urls()):
            if number >= limit:
                break
            patent = parce(url)
            # ...
            yield patent

    def parsed_patents_csv(self) -> DataFrame:
        # 1. создать новый DataFrame
        # df_out = DataFrame

        # 2. Перебираешь все строки csv файла, который подали в этот класс
        for old_row in self.rows():
            new_row = old_row


        # 2.1. Добавить в DataFrame новую строку из старого CSV

        # 2.2. Запустить парсер для этого патента
        # patent: PatentDocument = parce(url)

        # 2.3. Заполнить строку новыми данными из объекта парсера
        # new_row.add('abstract', patent.abstract)

        # 2.4. Сохранить строку в новом DataFrame
        # df_out.add(new_row)

        # 3. Вернуть DataFrame
        # return df_out
        ...

if __name__ == '__main__':
    csv = CSVPatents('str')

    for patent in csv.all(limit=5):
        print(patent)

