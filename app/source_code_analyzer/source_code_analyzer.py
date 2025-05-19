from app.entities.api_list import APIList
from app.source_code_analyzer.python_analyzer import PythonAnalyzer
from app.source_code_analyzer.source_code_fetcher import SourceCodeFetcher

class SourceCodeAnalyzer:
    def __init__(self):
        self.jsAnalyzer = None  # Assign the JavaScriptAnalyzer instance
        self.pythonAnalyzer = None  # Assign the PythonAnalyzer instance
        self.sourceCodeFetcher = SourceCodeFetcher() # Assign the SourceCodeFetcher instance

    def analyze(self, api_list: APIList):
        # Logic to analyze the source code
        moduleList = api_list.getModuleNames() # Get the list of modules from the APIList object
        sourceCodeIDList = self.sourceCodeFetcher.createAPIList(moduleList) # Get the source code IDs from searchcode API

        # TODO: Implement logic to identify the programming language from the APIList. Currently only supports Python.
        self.pythonAnalyzer = PythonAnalyzer(api_list)
        for id in sourceCodeIDList:
            rawCode = self.sourceCodeFetcher.getRawCodeString(id)
            api_list = self.pythonAnalyzer.analyze(rawCode) # APIList object is passed to the analyzer and appearences for each object are updated for each ID.
        
        return api_list