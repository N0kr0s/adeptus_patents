import dataclasses


@dataclasses.dataclass
class PatentDocument:
    """
    Как использовать:
    ```python
    df_out = PatentDocument(
        url=<something>,
        abstract=...,
        ...
    )
    ```

    Структура:
    :abstract: Аннотация патента (на странице патента). Должна содержать только текст (тело) аннотации.
    :images: Список ссылок на изображения, которые встречаются на странице патента.
    :classifications: Список классификации патента. Должен содержать видимый текст (вместе с уникальным номером) классификации.
    :description: Описание, которое обычно находится ниже аннотации.
    :claims: То, что лежит рядом с описанием патента.
    :status: Статус патента (обычно `Active`).
    :inventor: Список с именами людей (если человек один, то список будет с одним элементом).
    :patent_citation_number: Число цитирований патента. Обычно находится в круглых скобочках справа от подзаголовка "Patent Citations".
    :cited_number: Аналогично с цитированием, просто число.
    :priority_applications_number: Аналогично, число ("Priority Applications").
    :apps_claiming_priority_number: Аналогично, число ("Apps Claiming Priority").

    """
    abstract: str
    images: list[str]
    classifications: list[str]
    description: str
    claims: str
    status: str
    inventor: list[str]
    patent_citation_number: int
    cited_number: int
    priority_applications_number: int
    apps_claiming_priority_number: int