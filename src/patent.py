import dataclasses


@dataclasses.dataclass
class PatentDocument:
    """
    df_out = PatentDocument(
        url=<something>,
        abstract=...,
        ...
    )
    """
    url: str
    abstract: str
    images: list[str]
    classifications: list[str]
    description: str
    claims: str
    status: str
    inventor: list[str]
    patent_citations_value: int
    cited_value: int
    priority_applications_value: int
    apps_claiming_priority_value: int