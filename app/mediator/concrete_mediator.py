from app.entities.api_list import APIList
from app.doc_parser.documentation_parser import DocumentationParser
from app.source_code_analyzer.source_code_analyzer import SourceCodeAnalyzer
from app.ranking_component.ranking_component import RankingComponent

class ConcreteMediator:
    def __init__(self):
        self.apiList = APIList()
        self.docParser = DocumentationParser()
        self.sourceCodeAnalyzer = SourceCodeAnalyzer()
        self.rankingComponent = RankingComponent()

    def beginDocParser(self):
        # Start documentation parsing
        self.apiList = self.docParser.submitURL("some_url")

    def beginSourceCodeAnalyzer(self):
        # Start source code analysis
        self.sourceCodeAnalyzer.analyze(self.apiList)

    def beginRanker(self):
        # Start ranking
        return self.rankingComponent.createJSON()
