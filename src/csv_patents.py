from concurrent.futures import ThreadPoolExecutor, as_completed
import dataclasses
import os

import pandas as pd

from src.parser import parse
from src.patent import PatentDocument
from src.config import (
    DATASET_PATH,
    OUT_CSV_PATH,
    MAX_WORKERS,
    SAVE_EVERY,
)


class CSVPatents:

    def __init__(self, path: str):
        self._path = path

    def rows_filling(
        self,
        patent: PatentDocument,
        old_row: dict,
    ) -> dict:
        """
        Объединяет исходную строку CSV
        с данными, полученными из страницы патента.
        """

        patent_dict = dataclasses.asdict(patent)

        return {
            **old_row,
            **patent_dict,
        }

    def rows(self):
        """
        Читает исходный CSV.
        """

        df = pd.read_csv(self._path)

        for _, row in df.iterrows():
            yield row.to_dict()

    def load_completed(self):
        """
        Загружает уже обработанные патенты
        из OUT_CSV_PATH.

        Возвращает:
            completed_ids — множество обработанных ID
            completed_rows — уже сохранённые строки
        """

        if not os.path.exists(OUT_CSV_PATH):
            print(
                "\nФайл результатов не найден."
                "\nНачинаем обработку с нуля."
            )

            return set(), []

        try:
            df = pd.read_csv(OUT_CSV_PATH)

        except Exception as e:
            print(
                f"\nНе удалось прочитать "
                f"{OUT_CSV_PATH}: {e}"
            )

            return set(), []

        if df.empty or "id" not in df.columns:
            print(
                "\nФайл результатов пустой "
                "или не содержит столбец id."
            )

            return set(), []

        completed_ids = set(
            df["id"]
            .dropna()
            .astype(str)
        )

        completed_rows = df.to_dict(
            orient="records"
        )

        print(
            f"\nНайден существующий результат:"
            f" {len(completed_rows)} патентов."
        )

        return completed_ids, completed_rows

    def parse_row(self, old_row: dict):
        """
        Обрабатывает один патент.
        """

        try:

            patent: PatentDocument = parse(
                old_row["url"]
            )

            if patent is None:
                return None, old_row["id"]

            new_row = self.rows_filling(
                patent,
                old_row,
            )

            return new_row, None

        except Exception as e:

            print(
                f"\nОшибка при обработке "
                f"{old_row.get('url')}: {e}"
            )

            return None, old_row.get("id")

    def save_results(self, rows_list):
        """
        Сохраняет текущий checkpoint.
        """

        columns = [
            "id",
            "title",
            "assignee",
            "inventor/author",
            "priority date",
            "filing/creation date",
            "publication date",
            "grant date",
            "url",
            "abstract",
            "images",
            "classifications",
            "description",
            "claims",
            "status",
            "inventor",
            "patent_citation_number",
            "cited_number",
            "priority_applications_number",
        ]

        df_out = pd.DataFrame(
            rows_list,
            columns=columns,
        )

        os.makedirs(
            os.path.dirname(OUT_CSV_PATH),
            exist_ok=True,
        )

        df_out.to_csv(
            OUT_CSV_PATH,
            index=False,
        )

        return df_out

    def parsed_patents_csv(self):

        # =========================================================
        # 1. Загружаем исходные строки
        # =========================================================

        rows = list(self.rows())

        total = len(rows)

        print(
            f"\nВсего патентов в dataset: {total}"
        )

        # =========================================================
        # 2. Загружаем предыдущий checkpoint
        # =========================================================

        completed_ids, completed_rows = (
            self.load_completed()
        )

        # =========================================================
        # 3. Оставляем только необработанные
        # =========================================================

        rows_to_process = []

        for row in rows:

            row_id = str(row["id"])

            if row_id not in completed_ids:
                rows_to_process.append(row)

        remaining = len(rows_to_process)

        print(
            f"Уже обработано: "
            f"{len(completed_ids)}"
        )

        print(
            f"Осталось обработать: "
            f"{remaining}"
        )

        print(
            f"Одновременных запросов: "
            f"{MAX_WORKERS}"
        )

        print(
            f"Сохранение каждые: "
            f"{SAVE_EVERY}"
        )

        # =========================================================
        # 4. Если всё уже обработано
        # =========================================================

        if remaining == 0:

            print(
                "\nВсе патенты уже обработаны."
            )

            return self.save_results(
                completed_rows
            )

        # =========================================================
        # 5. Продолжаем обработку
        # =========================================================

        rows_list = completed_rows.copy()

        completed_this_run = 0
        successful = 0
        failed = 0

        try:

            with ThreadPoolExecutor(
                max_workers=MAX_WORKERS
            ) as executor:

                futures = {
                    executor.submit(
                        self.parse_row,
                        row,
                    ): row
                    for row in rows_to_process
                }

                for future in as_completed(
                    futures
                ):

                    new_row, error_id = (
                        future.result()
                    )

                    completed_this_run += 1

                    if new_row is not None:

                        rows_list.append(
                            new_row
                        )

                        successful += 1

                    else:

                        failed += 1

                    print(
                        f"\r"
                        f"Текущий запуск: "
                        f"{completed_this_run}/"
                        f"{remaining} | "
                        f"успешно: {successful} | "
                        f"ошибок: {failed}",
                        end="",
                        flush=True,
                    )

                    # =================================================
                    # Checkpoint
                    # =================================================

                    if (
                        completed_this_run
                        % SAVE_EVERY == 0
                    ):

                        print(
                            "\n\n"
                            "Сохранение checkpoint..."
                        )

                        self.save_results(
                            rows_list
                        )

                        print(
                            f"Сохранено патентов: "
                            f"{len(rows_list)}"
                        )

                        print(
                            f"Файл: "
                            f"{OUT_CSV_PATH}"
                        )

        except KeyboardInterrupt:

            print(
                "\n\n"
                "Получен Ctrl+C."
            )

            print(
                "Сохраняем текущие результаты..."
            )

            self.save_results(
                rows_list
            )

            print(
                f"Сохранено: "
                f"{len(rows_list)} патентов."
            )

            print(
                "При следующем запуске "
                "обработка продолжится автоматически."
            )

            return pd.DataFrame(rows_list)

        # =========================================================
        # 6. Финальное сохранение
        # =========================================================

        print(
            "\n\n"
            "Обработка завершена."
        )

        print(
            f"Успешно: {successful}"
        )

        print(
            f"Ошибок: {failed}"
        )

        print(
            "Финальное сохранение..."
        )

        df_out = self.save_results(
            rows_list
        )

        print(
            f"Всего сохранено: "
            f"{len(df_out)}"
        )

        return df_out


if __name__ == "__main__":

    csv = CSVPatents(
        DATASET_PATH
    )

    result_df = (
        csv.parsed_patents_csv()
    )

    print(
        result_df.head()
    )