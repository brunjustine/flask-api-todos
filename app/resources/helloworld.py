from flask import request
from flask_restful import Resource, abort

class HelloWorldResource(Resource):

    def get(self):
        return {'data':'Hello World !'}, 200

class HelloWorldResourceNameToken(Resource):

    def get(self):
        url_args = request.args
        try:
            name = url_args['name']
            return {'data':'Hello ' + name + ' !'}, 200
        except:
            abort(400)


class HelloWorldResourceNameURL(Resource):

    def get(self, name):
        return {'data':'Hello ' + name + ' !'}, 200

class HelloWorldResourceNames(Resource):

    def get(self, count):
        return {'data': list(map(lambda x: str(x+1) + ': Hello world !', range(0, count)))}, 200
