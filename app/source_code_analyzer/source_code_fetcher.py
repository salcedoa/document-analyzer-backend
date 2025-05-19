# Collects source code from SearchCode API
import requests
from urllib.parse import urljoin
from app.entities.api_list import APIList

class SourceCodeFetcher:
    def __init__(self):
        self.base_url = "https://searchcode.com/api/codesearch_I/"

    # Create a list of SearchCode IDs returned from querying import statements for each module.
    def createAPIList(self, moduleList):
        idList = []
        # Add modules to the APIList object
        for module in moduleList:
            tempIDList = self._searchCode('python', f'"import {module}"') 
            if tempIDList:
                for id in tempIDList:
                    if id not in idList:
                        idList.append(str(id))
            else:
                print("First search returned no results.")
        
        # Second query for "from module import" statements
        for module in moduleList:
            tempIDList = self._searchCode('python', f'"from {module} import"') 
            if tempIDList:
                for id in tempIDList:
                    if id not in idList:
                        idList.append(str(id))
            else:
                print("Second search returned no results.")
        
        if len(idList) == 0:
            print("No IDs found in the searchcode API.")
            return None
        else:
            return idList
    
    # Returns a list of IDs for the source code that matches the search term.
    def _searchCode(self, lang, query):
        params = {
            'q': query,  # Simplified search term
            'lan': lang,  # Language filter (Only Python)
            'p': 1,  # Page number
            'per_page': 100,  # Results per page
        }

        # Send request to searchcode API
        response = requests.get(self.base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            search_results = response.json()
            if search_results['results']:
                resultIDList = []
                for result in search_results['results']:
                    #print(f"Repository: {result.get('repo')}")
                    #print(f"File URL: {result.get('url')}\n")
                    resultIDList.append(result.get('id')) # Collect all resulting IDs in a list to run through getRawCodeString later.
                return resultIDList
            else:
                print("No searchcode results found.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    
    # Returns raw code as a string. To be passed to the analyzer.
    def getRawCodeString(self, id):
        base_url = 'https://searchcode.com/api/result/'
        response = requests.get(urljoin(base_url, id))

        if response.status_code == 200:
            search_results = response.json()
            if search_results['code']:
                rawCode = search_results['code']
            else:
                print("No results found.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
        
        return rawCode