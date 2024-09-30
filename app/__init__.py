from flask import Flask, request
from flask_restx import Api, Resource, fields
from app.mediator.concrete_mediator import ConcreteMediator

# Initialize Flask and Flask-RESTx
app = Flask(__name__)
api = Api(app, version='1.0', title='Documentation Analyzer API',
          description='The backend component for the documentation analyzer.')

# Define a namespace
ns = api.namespace('analyze', description='Operations related to analysis')

url_model = api.model('URLModel', {
    'url': fields.String(required=True)
})

# Define the resource for running the analysis
@ns.route('/start')
class StartAnalysis(Resource):
    @api.expect(url_model)
    def post(self):
        # Get URL from request
        data = request.json
        url = data.get('url')
        if not url:
            return {'message': 'URL is required'}, 400

        # Initialise mediator
        mediator = ConcreteMediator(url)
        apiList = mediator.beginAnalysis() # returns either apiList or None
        if apiList:
            return {'message': 'Analysis started', 'status': 'In Progress'}, 202
        else:
            return {'message': 'Input not able to be analyzed', 'status': 'Failed'}, 400

@ns.route('/status/<string:task_id>')
class AnalysisStatus(Resource):
    def get(self, task_id):
        # Polling method: Frontend will periodically check status.
        # Function from mediator object to check status.
        
        # Placeholder: Completed
        return {'task_id': task_id, 'status': 'Completed'}, 200

@ns.route('/result<string:task_id>')
class AnalysisResult(Resource):
    def get(self, task_id):
        data = request.json
        url = data.get('task_id')
        
        # Return placeholder data as defined in fronetend app.
        # Mediator function will return the proper JSON data straight from the ranker component.
        sample_data = {
            "ID": 55,
            "Classes": [
                {"rank": 1, "name": "Book", "link": "http://docs.example.org/book"},
                {"rank": 2, "name": "Member", "link": "http://docs.example.org/member"},
                {"rank": 3, "name": "Loan", "link": "http://docs.example.org/loan"},
                {"rank": 4, "name": "Catalog", "link": "http://docs.example.org/catalog"},
                {"rank": 5, "name": "Member", "link": "http://docs.example.org/member"}
            ],
            "Methods": [
                {"rank": 1, "name": "getBook", "link": "http://docs.example.org/getBook"},
                {"rank": 2, "name": "addMember", "link": "http://docs.example.org/addMember"},
                {"rank": 3, "name": "issueLoan", "link": "http://docs.example.org/issueLoan"},
                {"rank": 4, "name": "updateCatalog", "link": "http://docs.example.org/updateCatalog"},
                {"rank": 5, "name": "removeMember", "link": "http://docs.example.org/removeMember"}
            ]
        }
        return sample_data, 200

# Add the namespace to the API
api.add_namespace(ns)

# Simple health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return "Server is running!"
