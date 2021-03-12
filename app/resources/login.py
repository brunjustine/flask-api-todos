from flask import request
from flask_restful import Resource, reqparse, abort
import hashlib, binascii, os
import jwt
from app.utils.utils import *
from app.resources.accounts import *
from app.services.accountsService import USERS

key = "secret"

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
        body_parser.add_argument('login', type=str, required=True, help="Missing the login of the user")
        body_parser.add_argument('hash', type=str, required=True, help="Missing the password associated to the user login")
        args = body_parser.parse_args(strict=True) # Accepted only if these two parameters are strictly declared in body else raise exception
        
        try:
            user = args['login']
            abort_if_user_doesnt_exist(user)
            password_hash = args['hash']
            return login(user, password_hash)
        except Exception as e:
            return "{}".format(e)

# Hash for "password"
def login(login, hash_send):
    hash = get_hash_by_login(login)
    key = hash['password']['key']
    #<---- TO DELETE 
    salt = hash['password']['salt']
    new_key = hashlib.pbkdf2_hmac('sha256', hash_send.encode('utf-8'), salt.encode('ascii'), 100000)
    new_hash = binascii.hexlify(new_key).decode('ascii')
    ## ---->
    if login == 'brunjustin' and new_hash == key:
        token = get_token(login)
        return return_message({"token":token}, 200, " Logged in successfully")
    else:
        return return_message({},401, " Cannot log in, check your credentials and retry")

def abort_if_user_doesnt_exist(user_login):
    user_logins = get_logins()
    if user_login not in user_logins:
        return_message({},401, " Cannot log in, check your credentials and retry")
         
def get_hash_by_login(user_login):
    return list(filter(lambda user : user['login']==user_login, USERS))[0]
        
def get_token(user):
    return jwt.encode({"login":user}, key, algorithm="HS256")

