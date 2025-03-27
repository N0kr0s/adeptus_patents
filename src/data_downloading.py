import os
import requests
import time


def download_dataset(url, save_dir, file_name, retries=5, delay=5):
    # Проверка наличия директории
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)  # Создание директории, если она не существует
        print(f"Создана директория: {save_dir}")

    # Путь к файлу
    file_path = os.path.join(save_dir, file_name)

    # Проверка, существует ли файл
    if os.path.exists(file_path):
        print(f"Файл {file_name} уже существует в {save_dir}.")
        return

    # Скачивание файла
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка на ошибки HTTP

            # Запись содержимого в файл
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Файл успешно скачан и сохранён как {file_name} в {save_dir}.")
            return

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP ошибка: {http_err}")
            if response.status_code in [503, 429]:
                print(f"Попробуйте снова через {delay} секунд...")
                time.sleep(delay)  # Ждем перед повторной попыткой

                #503 Service Unavailable — сервер временно недоступен
                #429 Too Many Requests — превышен лимит запросов
            else:
                print("Не удается скачать файл из-за ошибки HTTP.")
                return
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при скачивании файла: {e}")
            return

    print("Все попытки исчерпаны. Не удалось скачать файл.")

if __name__ == '__main__':
    # Параметры
    url = "https://patents.google.com/xhr/query?url=language%3DSPANISH&exp=&download=true"
    save_directory = "data/"
    file_name = "gp.csv"

    # Вызов функции
    download_dataset(url, save_directory, file_name)