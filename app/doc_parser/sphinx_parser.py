from app.entities.api_list import APIList
from app.entities.api_object import APIObject

from typing import Optional
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

class SphinxParser:
    def __init__(self, url):
        self.list = APIList()
        self.url = url

    def parseURL(self) -> Optional[APIList]:
        # Logic to parse Sphinx documentation
        
        # 1. Collect module names and links.
        modules = self._collectModules()
        if len(modules) == 0:
            print("Module list was empty")
            return None

        # 2. Go though each module page and collect classes and methods
        classList = []
        methodList = []
        for name, modLink in modules:
            modulePage = urljoin(self.url, modLink)
            response = requests.get(modulePage)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find elements pertaining to classes (Containing classes and methods)
            classElements = soup.find_all(class_='py class')
            for element in classElements:
                classLink = element.find(class_='headerlink')['href']
                className = element.find(class_='sig sig-object py').get_text().replace('¶', '')
                if className.split()[0] == 'class':
                    # "Class " is cut from the name.
                    classList.append((className[7:], urljoin(modulePage, classLink)))
            
                    # Collect methods
                    singleName = element.find(class_='sig-name descname').get_text()
                    methodList.extend(self._collectMethods(element, singleName))     

        # 3. Add classes to APIList
        for name, link in classList:
            tempObject = APIObject(name, "class", 0, link)
            self.list.recordAPIObject(tempObject)

        # 4. Add methods to APIList
        for name, link in methodList:
            tempObject = APIObject(name, "method", 0, link)
            self.list.recordAPIObject(tempObject)
        
        return self.list
    
    def _collectModules(self) -> Optional[list[tuple[str, str]]]:
        modulePage = urljoin(self.url, "py-modindex.html")
        response = requests.get(modulePage)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Find the table with the class 'modindextable'
        moduleTable = soup.find(class_='modindextable')
        if not moduleTable:
            return None # Module table not found
        
        # 2. Collect all <a> elements inside the table
        moduleElements = moduleTable.find_all('a')

        # 3. Extract the name and link from each module elememt.
        modules = []
        if moduleElements:
            for e in moduleElements:
                moduleName = e.get_text()
                moduleLink = e['href']
                modules.append((moduleName, moduleLink))
        
        return modules

    # Collect methods from inside a class object.
    def _collectMethods(self, classElement, className) -> list[tuple[str, str]]:
        modulePage = urljoin(self.url, "py-modindex.html")
        moduleMethodsList = []
        methodObjects = classElement.find_all(class_='py method')
        for method in methodObjects:
            methodName = method.find('span', class_='sig-name').get_text()
            methodLink = method.find(class_='headerlink')['href']
            moduleMethodsList.append((className + '.' + methodName, urljoin(modulePage, methodLink)))
    
        return moduleMethodsList
