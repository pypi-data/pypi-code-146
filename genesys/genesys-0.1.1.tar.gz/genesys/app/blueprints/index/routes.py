from flask import Blueprint
from flask_restful import Api, Resource
from genesys import __version__

index = Blueprint('index', __name__)
api = Api(index)

class Index(Resource):
    def get(self):
        return {"api": "eaxum_zou", "version": __version__}


api.add_resource(Index, '/')