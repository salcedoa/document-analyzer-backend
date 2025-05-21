from app.entities.api_list import APIList
from app.doc_parser.documentation_parser import DocumentationParser
from app.source_code_analyzer.source_code_analyzer import SourceCodeAnalyzer
from app.ranking_component.ranking_component import RankingComponent

class ConcreteMediator:
    def __init__(self, url):
        #self.docParser = DocumentationParser()
        #self.sourceCodeAnalyzer = SourceCodeAnalyzer()
        #self.rankingComponent = RankingComponent()
        self.url = url
        self.currentStage = 1
    
    # Called by the first POST request /start
    def beginAnalysis(self):
        return self._beginDocParser()
    
    def checkStatus(self):
        # currentStage gets updates inside private methods
        return self.currentStage

    def getAPIList(self):
        # Returns the APIList object
        return self.apiList

    def _beginDocParser(self):
        # Start documentation parsing
        # Doc parser component returns a populated APIList object.
        self.docParser = DocumentationParser()
        self.apiList = self.docParser.submitURL(self.url) # Note that URL must end in a forward slash to work.
        del self.docParser

        if self.apiList:
            # Begin source code analysis
            self.currentStage = 2
            return self._beginSourceCodeAnalyzer()
        else:
            return None # API list creation failed

    def _beginSourceCodeAnalyzer(self):
        # Start source code analysis
        self.sourceCodeAnalyzer = SourceCodeAnalyzer()
        self.apiList = self.sourceCodeAnalyzer.analyze(self.apiList) # Returns APIList object
        if self.apiList:
            # Begin ranking
            self.currentStage = 3
            print(self.apiList.to_json())

            return self.apiList
        else:
            return None # Source code analysis failed

    def _beginRanker(self):
        # Start ranking
        return self.rankingComponent.createJSON()
