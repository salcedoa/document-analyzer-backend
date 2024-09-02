from .mkdocs_parser import MkDocsParser
from .sphinx_parser import SphinxParser

class DocumentationParser:
    def __init__(self):
        self.MkDocs = MkDocsParser()
        self.Sphinx = SphinxParser()

    def submitURL(self, url: str) -> bool:
        # Determine which parser to use based on the URL or file type
        if "mkdocs" in url:
            return self.MkDocs.parseURL(url)
        elif "sphinx" in url:
            return self.Sphinx.parseURL(url)
        return False
