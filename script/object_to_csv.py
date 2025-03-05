class MoveToCSV:
    def __init__(self, url):
        self.url = url  # URL задается при создании объекта
        self.abstract = None
        self.images = None
        self.classifications = None
        self.description = None
        self.claims = None
        self.status = None
        self.inventor = None
        self.patent_citations_value = None  # Patent Citations value
        self.cited_value = None  # Cited value
        self.priority_applications_value = None  # Priority Applications value
        self.apps_claiming_priority_value = None  # Applications Claiming Priority value
        self.meta_description = None
        self.citation_patent_application_number = None
        self.dc_contributor = None

