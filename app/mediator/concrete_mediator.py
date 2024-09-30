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
        return self._beginDocParser(self.url)
    
    def checkStatus(self, id):
        # currentStage gets updates inside private methods
        return self.currentStage


    def _beginDocParser(self, url):
        # Start documentation parsing
        # Doc parser component returns a populated APIList object.
        self.docParser = DocumentationParser()
        self.apiList = self.docParser.submitURL(self.url)
        del self.docParser

        if self.apiList:
            return self.apiList
        else:
            return None # API list creation failed

        # TODO: Begin source code analysis
        self.currentStage = 2

    def _beginSourceCodeAnalyzer(self):
        # Start source code analysis
        self.sourceCodeAnalyzer.analyze(self.apiList)

    def _beginRanker(self):
        # Start ranking
        return self.rankingComponent.createJSON()
