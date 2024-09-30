from .mkdocs_parser import MkDocsParser
from .sphinx_parser import SphinxParser
from app.entities.api_list import APIList

import requests
from requests.exceptions import RequestException
import json
from typing import Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class DocumentationParser:
    
    def _checkDocType(self, url:str) -> Optional[str]:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except RequestException as e:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        # Check for ReadTheDocs JSON data
        script_tag = soup.find('script', {'type': 'application/json', 'id': 'READTHEDOCS_DATA'})
        if script_tag:
            script_content = json.loads(script_tag.string)  
            if script_content.get('builder') == 'sphinx':
                return "sphinx"
            if script_content.get('builder') == 'mkdocs':
                return "mkdocs"
        if soup.find('div', {'class': 'sphinxsidebar'}) or soup.find('meta', {'name': 'generator', 'content': 'Sphinx'}): 
            return "sphinx"
        
        # Check for MkDocs specific markers
        meta_tag = soup.find('meta', {'name': 'generator'})
        if meta_tag and 'mkdocs' in meta_tag.get('content', ''):
            return "mkdocs"

        return None
        # TODO: Try again with "docs." URL prefix
        

    def submitURL(self, url: str) -> Optional[APIList]:
        # Determine which parser to use based on the site.
        docType = self._checkDocType(url)
        if not docType:
            print("Unknown documentation format")
            return None # Unknown documentation format

        if docType == "mkdocs":
            #return self.mkdocsParser.parseURL(url)
            return None # Possibly custom message, not currently supported.
        elif docType == "sphinx":
            self.sphinxParser = SphinxParser(url)
            return self.sphinxParser.parseURL()
        return None