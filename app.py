# coding: utf-8
from flask import Flask
from flask_restful_swagger_2 import Api
# The line below needs to be uncommented when debugging
# from flask_cors import CORS
from routes import setup_routes

app = Flask(__name__)

api = Api(app, api_version='1.0', api_spec_url='/api/specs')
setup_routes(api)

from data_access.data_access_base import DataAccessBase
DataAccessBase.initialize()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5234)