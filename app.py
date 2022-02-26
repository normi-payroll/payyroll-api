import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
from resources.Data import Data
from resources.Image import UploadAPI

app = Flask(__name__)
api = Api(app)

JWT_SECURITY_KEY = os.getenv('JWT_SECURITY_KEY')
jwt = JWTManager(app)
@app.after_request

def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

api.add_resource(Data, '/api/data/<string:col>/<string:query>')
#api.add_resource(Data, '/api/data/<string:col>/<string:query>')
if __name__ == '__main__':
    app.run(debug=True, port="8080", host="0.0.0.0")