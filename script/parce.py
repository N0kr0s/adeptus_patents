import pandas as pd

# Путь к файлу
file_path = '..data/gp-search-20250301-010925.xlsx'

# Чтение Excel файла, пропуская первую строку
df = pd.read_excel(file_path, skiprows=1)

# Переименование столбцов (если они не читаются корректно)
df.columns = [
    'id', 'title', 'assignee', 'inventor/author', 'priority date',
    'filing/creation date', 'publication date', 'grant date',
    'result link', 'representative figure link'
]

# Очистка DataFrame от строк с пустыми значениями в столбце 'result link'
df = df[df['result link'].notna()]

# Извлечение списка ссылок из столбца 'result link'
result_links = df['result link'].tolist()

# Вывод ссылок
for link in result_links:
    print(link)