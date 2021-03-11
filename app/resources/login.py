from flask import request
from flask_restful import Resource, reqparse, abort

class LoginResource(Resource):

    def get(self):
        url_args = request.args
        try:
            user = url_args['user']
            password_hash = url_args['pwd']
            return self.login(user, password_hash)
        except:
            abort(400)

    def post(self):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('user', type=str, required=True, help="Missing the login of the user")
        body_parser.add_argument('pwd', type=str, required=True, help="Missing the password associated to the user login")
        args = body_parser.parse_args(strict=True) # Accepted only if these two parameters are strictly declared in body else raise exception
        try:
            user = args['user']
            password_hash = args['pwd']
            return login(user, password_hash)
        except:
            abort(400)

# Hash for "password"
def login(login, hash):
    if (login == 'login' and hash == '5f4dcc3b5aa765d61d8327deb882cf99'):
        return { "message" : "Logged in successfully" }, 200
    else:
        return { "message" : "Cannot log in, check your credentials and retry"}, 401

