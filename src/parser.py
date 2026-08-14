import time
import requests

from bs4 import BeautifulSoup

from src.patent import PatentDocument
from src.config import REQUEST_TIMEOUT, MAX_RETRIES


def parse(url: str) -> PatentDocument | None:
    for attempt in range(1, MAX_RETRIES + 1):

        try:

            response = requests.get(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (X11; Linux x86_64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/131.0.0.0 Safari/537.36"
                    ),
                    "Accept": (
                        "text/html,application/xhtml+xml,"
                        "application/xml;q=0.9,*/*;q=0.8"
                    ),
                    "Accept-Language": "es,en;q=0.8",
                },
                timeout=REQUEST_TIMEOUT,
            )

            print(
                f"\nURL: {url}"
            )

            print(
                f"HTTP status: {response.status_code}"
            )

            print(
                f"Response size: "
                f"{len(response.content)} bytes"
            )

            if response.status_code == 200:
                break

            print(
                f"Попытка {attempt}/{MAX_RETRIES} "
                f"завершилась статусом "
                f"{response.status_code}"
            )

        except requests.RequestException as e:

            print(
                f"\nОшибка запроса "
                f"(попытка {attempt}/{MAX_RETRIES}): "
                f"{e}"
            )

            if attempt == MAX_RETRIES:
                return None

            # Небольшая пауза перед повтором
            time.sleep(attempt * 2)

    else:
        return None

    print(f"URL: {url}")
    print(f"HTTP status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"Response size: {len(response.content)} bytes")

    if response.status_code != 200:
        print("Ответ сервера:")
        print(response.text[:1000])
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Аннотация
    abstract_element = soup.find("div", class_="abstract")
    abstract = (
        abstract_element.get_text(strip=True)
        if abstract_element
        else None
    )

    # Изображения
    images = [
        img["src"]
        for img in soup.select('img[src*="patent"]')
        if img.get("src")
    ] or None

    # Классификации
    classifications_elements = soup.find_all(
        "li",
        itemprop="classifications",
    )

    classifications = (
        [
            element.get_text(strip=True)
            for element in classifications_elements
        ]
        if classifications_elements
        else None
    )

    # Описание
    description_element = soup.select_one(".description")

    description = (
        description_element.get_text(strip=True)
        if description_element
        else None
    )

    # Claims
    claims_elements = soup.select(".claims .claim")

    claims = (
        "\n".join(
            claim.get_text(strip=True)
            for claim in claims_elements
        )
        if claims_elements
        else None
    )

    # Изобретатели
    inventor_elements = soup.select(
        'dd[itemprop="inventor"]'
    )

    inventors = (
        [
            inventor.get_text(strip=True)
            for inventor in inventor_elements
        ]
        if inventor_elements
        else None
    )

    # Patent citations
    patent_citation_number = None

    family_cites_element = soup.find(
        "h2",
        string=lambda x: (
            x and "Family Cites Families" in x
        ),
    )

    if family_cites_element:
        text = family_cites_element.get_text(strip=True)

        try:
            patent_citation_number = int(
                text.split("(")[-1].strip(")")
            )
        except ValueError:
            pass

    # Cited number
    cited_number = None

    cited_number_element = soup.find(
        "h2",
        string=lambda x: (
            x and "Families Citing this family" in x
        ),
    )

    if cited_number_element:
        text = cited_number_element.get_text(strip=True)

        try:
            cited_number = int(
                text.split("(")[-1].strip(")")
            )
        except ValueError:
            pass

    # Priority applications
    priority_applications_number = None

    priority_applications = soup.find(
        "h2",
        string=lambda x: (
            x and "Applications Claiming Priority" in x
        ),
    )

    if priority_applications:
        text = priority_applications.get_text(strip=True)

        try:
            priority_applications_number = int(
                text.split("(")[-1].strip(")")
            )
        except ValueError:
            pass

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
    )

    return patent


if __name__ == "__main__":
    url = (
        "https://patents.google.com/"
        "patent/ES2557055T3/es"
    )

    patent = parse(url)

    if patent:
        print("\nИнформация о патенте:")
        print(f"Аннотация: {patent.abstract}")
        print(f"Изображения: {patent.images}")
        print(f"Классификации: {patent.classifications}")
        print(f"Описание: {patent.description}")
        print(f"Претензии: {patent.claims}")
        print(f"Изобретатели: {patent.inventor}")
        print(
            "Количество патентных цитат: "
            f"{patent.patent_citation_number}"
        )
        print(
            "Количество цитирований: "
            f"{patent.cited_number}"
        )
        print(
            "Количество приоритетных заявок: "
            f"{patent.priority_applications_number}"
        )
    else:
        print("Не удалось получить данные о патенте.")