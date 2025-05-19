from flask import Flask, request
from flask_restx import Api, Resource, fields
from uuid import uuid4
from app.mediator.concrete_mediator import ConcreteMediator
import threading

# Initialize Flask and Flask-RESTx
app = Flask(__name__)
api = Api(app, version='1.0', title='Documentation Analyzer API',
          description='The backend component for the documentation analyzer.')

# Define a namespace
ns = api.namespace('analyze', description='Operations related to analysis')

url_model = api.model('URLModel', {
    'url': fields.String(required=True)
})

task_store = {}  # Store task status and results

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
        
        # Create a unique task ID
        task_id = str(uuid4())
        print(f"Task ID: {task_id}")
        task_store[task_id] = {'status': 'In Progress', 'result': None} # Store task status in task_store dictionary

        def run_analysis(task_id, url):
            try:
                print(f"[{task_id}] Starting analysis for {url}")
                mediator = ConcreteMediator(url)  # instantiate mediator inside thread
                result_obj = mediator.beginAnalysis()
                print(f"[{task_id}] Analysis returned result")

                if result_obj:
                    result = result_obj.to_json()
                    task_store[task_id]['status'] = 'Completed'
                    task_store[task_id]['result'] = result
                    print(f"[{task_id}] Stored result")
                else:
                    task_store[task_id]['status'] = 'Failed'
                    print(f"[{task_id}] Analysis returned None")
            except Exception as e:
                task_store[task_id]['status'] = 'Failed'
                print(f"[{task_id}] Exception during analysis: {e}")

        threading.Thread(target=run_analysis, args=(task_id, url)).start()
        return {'message': 'Analysis started', 'status': 'In Progress', 'task_id': task_id}, 202

@ns.route('/status/<string:task_id>')
class AnalysisStatus(Resource):
    # Polling method: Frontend will periodically check status.
    def get(self, task_id):
        task = task_store.get(task_id)
        if not task:
            return {'message': 'Invalid task ID'}, 404
        return {'task_id': task_id, 'status': task['status']}, 200

@ns.route('/result/<string:task_id>')
class AnalysisResult(Resource):
    def get(self, task_id):
        task = task_store.get(task_id)
        if not task:
            return {'message': 'Invalid task ID'}, 404
        if task['status'] != 'Completed':
            return {'message': 'Task not complete', 'status': task['status']}, 202
        return {'result': task['result']}, 200

# Add the namespace to the API
api.add_namespace(ns)

# Simple health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return "Server is running!"
