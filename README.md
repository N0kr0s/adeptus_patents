# adeptus_patents
![image](https://github.com/user-attachments/assets/6e46b1a8-e84a-4960-9bbe-0854945df6e9)


Для работы далее по проекту (особенно учитывая, что мы все вместе должны суметь объяснить логику работы проекта) нужно будет изучить как минимум эти 2 основные библиотеки:

  1) BeautifulSoup (bs4):
   
    https://www.youtube.com/watch?v=vtizH9w0V7c&t=289s&ab_channel=%D0%A5%D0%B0%D1%83%D0%B4%D0%B8%D0%A5%D0%BE%E2%84%A2-%D0%9F%D1%80%D0%BE%D1%81%D1%82%D0%BE%D0%BE%D0%BC%D0%B8%D1%80%D0%B5IT%21
    https://www.youtube.com/watch?v=lOfm04oLD1U&ab_channel=PythonHubStudio
    https://pypi.org/project/beautifulsoup4/
    https://habr.com/ru/articles/544828/

  2) Pandas:
   
    https://www.youtube.com/watch?v=-sJxwvx0P20&t=276s&ab_channel=AlexanderErshov
    https://skillbox.ru/media/code/rabotaem-s-pandas-osnovnye-ponyatiya-i-realnye-dannye/
    https://pandas.pydata.org/docs/

  3) Python dict:
   
    https://skillbox.ru/media/code/slovari-v-python-chto-nuzhno-znat-i-kak-polzovatsya/

Юзаем сайт https://patents.google.com/?language=SPANISH и вытаскиваем из него url-ки (result link), переходим по ним через request, парсим всю инфу с этих url-ок к нам в датасет и всё гг вп

## Установка зависимостей
```bash
pip install -r requirements.txt