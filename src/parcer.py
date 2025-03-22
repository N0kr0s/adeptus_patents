import requests
from bs4 import BeautifulSoup
from patent import PatentDocument


def parse(url: str) -> PatentDocument:
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка при запросе URL: {url}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Извлечение данных
    abstract_element = soup.find('div', class_='abstract')
    abstract = abstract_element.text.strip() if abstract_element else None

    images = [img['src'] for img in soup.select('img[src*="patent"]')] or None

    classifications_elements = soup.find_all('li', itemprop='classifications')
    classifications = [inv.text.strip() for inv in classifications_elements] if classifications_elements else None

    description_element = soup.select_one('.description')
    description = description_element.text.strip() if description_element else None

    claims_elements = soup.select('.claims .claim')
    claims = "\n".join(claim.text.strip() for claim in claims_elements) if claims_elements else None

    inventor_elements = soup.select('dd[itemprop="inventor"]')
    inventors = [inv.text.strip() for inv in inventor_elements] if inventor_elements else None

    patent_citation_number = None  # Инициализируем переменную
    family_cites_element = soup.find('h2', string=lambda x: x and 'Family Cites Families' in x)
    if family_cites_element:
        family_cites_text = family_cites_element.get_text(strip=True)
        patent_citation_number = family_cites_text.split('(')[-1].strip(')')  # Получаем число из текста

    cited_number = None  # Инициализируем переменную
    cited_number_element = soup.find('h2', string=lambda x: x and 'Families Citing this family' in x)
    if cited_number_element:
        cited_number_object = cited_number_element.get_text(strip=True)
        cited_number = cited_number_object.split('(')[-1].strip(')')  # Получаем число из текста

    priority_applications_number = None  # Инициализируем переменную
    priority_applications = soup.find('h2', string=lambda x: x and 'Applications Claiming Priority' in x)
    if priority_applications:
        priority_applications_text = priority_applications.get_text(strip=True)
        priority_applications_number = priority_applications_text.split('(')[-1].strip(')')

    apps_claiming_priority_number = int(soup.select_one('.apps-claiming-priority').text.strip()) if soup.select_one(
        '.apps-claiming-priority') else None

    patent = PatentDocument(
        abstract=abstract,
        images=images,
        classifications=classifications,
        description=description,
        claims=claims,
        inventor=inventors,
        status="Active",
        patent_citation_number=patent_citation_number,
        cited_number=cited_number,
        priority_applications_number=priority_applications_number,
        apps_claiming_priority_number=apps_claiming_priority_number
    )

    return patent


if __name__ == '__main__':
    url = 'https://patents.google.com/patent/ES2557055T3/es#relatedApplications'
    patent = parse(url)
    if patent:
        print("Информация о патенте:")
        print(f"Аннотация: {patent.abstract}")
        print(f"Изображения: {patent.images}")
        print(f"Классификации: {patent.classifications}")
        print(f"Описание: {patent.description}")
        print(f"Претензии: {patent.claims}")
        print(f"Изобретатели: {patent.inventor}")
        print(f"Количество патентных цитат: {patent.patent_citation_number}")
        print(f"Количество цитирований: {patent.cited_number}")
        print(f"Количество приоритетных заявок: {patent.priority_applications_number}")
        print(f"Количество заявок, claiming priority: {patent.apps_claiming_priority_number}")
    else:
        print("Не удалось получить данные о патенте.")