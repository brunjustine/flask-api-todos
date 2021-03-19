from flask import request
from flask_restful import Resource, reqparse, abort
import jwt
from app import bcrypt
from app.utils.utils import *
from app.resources.accounts import *
from app.services.accountsService import USERS
from app.services.accountsService import connected_user

key = "secret"

class LoginResource(Resource):

    def get(self):
        url_args= request.args
        try:
            user = url_args['login']
            abort_if_user_doesnt_exist(login)
            user = get_by_login(login)
            password_hash = user['password']
            return return_message(password_hash,200,"")
        except:
            return return_message({},401,"")

    def post(self):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('login', type=str, required=True, help="Missing the login of the user")
        body_parser.add_argument('hash', type=str, required=True, help="Missing the password associated to the user login")
        args = body_parser.parse_args(strict=True) # Accepted only if these two parameters are strictly declared in body else raise exception
        try:
            user = args['login']
            password_hash = args['hash']
            abort_if_user_doesnt_exist(user)
        except:
            return return_message({},400,"")
        try:
            return login(user, password_hash)
        except Exception as e:
            return return_message({},401,"{}".format(e))

# Hash for "password"
def login(login, pwd)-> Dict:
    db_Login = get_by_login(login)
    is_hash = bcrypt.check_password_hash(db_Login['password'], pwd)
    if login == db_Login['login'] and is_hash:
        token = get_token(login)
        connected_user = {"login":login}
        return return_message({"token":token}, 200, " Logged in successfully")
    else:
        return return_message({},401, " Cannot log in, check your credentials and retry")

def abort_if_user_doesnt_exist(user_login):
    user_logins = get_logins()
    if user_login not in user_logins:
        return_message({},401, " Cannot log in, check your credentials and retry")
         
def get_by_login(user_login):
    return list(filter(lambda user : user['login']==user_login, USERS))[0]
        
def get_token(user):
    return jwt.encode({"login":user}, key, algorithm="HS256")
    