from flask import Flask
from flask_restx import Api, Resource
from app.mediator.concrete_mediator import ConcreteMediator

# Initialize Flask and Flask-RESTx
app = Flask(__name__)
api = Api(app, version='1.0', title='Documentation Analyzer API',
          description='A simple API to analyze documentation and source code')

# Define a namespace
ns = api.namespace('analyze', description='Operations related to analysis')

# Define the resource for running the analysis
@ns.route('/run')
class RunAnalysis(Resource):
    def get(self):
        mediator = ConcreteMediator()
        mediator.beginDocParser()
        mediator.beginSourceCodeAnalyzer()
        result = mediator.beginRanker()
        return result

# Add the namespace to the API
api.add_namespace(ns)

# Simple health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return "Server is running!"
