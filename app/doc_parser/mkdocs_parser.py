from app.entities.api_list import APIList

class MkDocsParser:
    def __init__(self):
        self.list = APIList()

    def parseURL(self, url: str) -> APIList:
        # Logic to parse MkDocs documentation
        return self.list
