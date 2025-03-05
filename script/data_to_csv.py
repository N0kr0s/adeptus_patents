import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Ошибка запроса: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при получении HTML: {e}")
        return None

url = "https://patents.google.com/patent/ES2932173T3/es?language=SPANISH&oq=language:SPANISH"
html_content = fetch_html(url)

if html_content:
    soup = BeautifulSoup(html_content, 'html.parser')

    # Парсинг метатегов
    title = soup.find('meta', {'name': 'DC.title'})
    title = title['content'].strip() if title and 'content' in title.attrs else None

    publication_number = soup.find('meta', {'name': 'citation_patent_application_number'})
    publication_number = publication_number['content'].strip() if publication_number and 'content' in publication_number.attrs else None

    # Парсинг абстракта
    abstract_div = soup.find('div', {'id': 'abstract'})
    abstract = ' '.join([p.text.strip() for p in abstract_div.find_all('p')]) if abstract_div else None

    # Парсинг классификаций
    classifications = []
    classification_section = soup.find('section', {'id': 'classifications'})
    if classification_section:
        for item in classification_section.find_all('li', recursive=False):
            code = item.find('span', {'class': 'code'})
            desc = item.find('span', {'class': 'description'})
            if code and desc:
                classifications.append({
                    'code': code.text.strip(),
                    'description': desc.text.strip()
                })

    # Парсинг описания
    description_section = soup.find('section', {'id': 'description'})
    description = ' '.join([div.text.strip() for div in description_section.find_all('div')]) if description_section else None

    # Парсинг claims
    claims_section = soup.find('section', {'id': 'claims'})
    claims = [claim.text.strip() for claim in claims_section.find_all('div', {'class': 'claim-text'})] if claims_section else []

    # Парсинг статуса
    status = soup.find('div', {'class': 'status'})
    status = status.text.strip() if status else None

    # Вывод результатов
    print(f"Title: {title}")
    print(f"Publication Number: {publication_number}")
    print(f"Abstract: {abstract}")
    print("Classifications:")
    for c in classifications:
        print(f" - {c['code']}: {c['description']}")
    print(f"Description: {description}")
    print("Claims:")
    for claim in claims:
        print(f" - {claim}")
    print(f"Status: {status}")
else:
    print("Не удалось получить HTML")