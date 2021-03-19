from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any

from app.services.accountsService import USERS
from app.utils.utils import *

import hashlib, binascii, os


class AccountsManagementResource(Resource):
    def get(self):
        """
        Get all users account of the users services
        ---
        tags:
            - Flask API
        responses:
            200:
                description: JSON representing all the elements of the users service
        """
        return return_message(USERS,200)
    
    def post(self):
        """
        Add a new user to the users services
        ---
        tags:
            - Flask API
        parameters:
            - in: body
              name: attributes
              description: The login and password of the user
              schema:
                type: object
                required:
                    - login
                    - password
                properties:
                  login:
                    type: string
                  password:
                    type: string
        responses:
            201:
                description: JSON representing created user
            400:
                description: The parameters are missing or are not correct
        """
        body_parser = reqparse.RequestParser(bundle_errors=True)  # Throw all the elements that has been filled uncorrectly
        body_parser.add_argument('login', type=str, required=True, help="Missing the login of the user")
        body_parser.add_argument('password', type=str, required=True, help="Missing the password of the user")

        # Accepted only if these two parameters are strictly declared in body else raise exception
        args = body_parser.parse_args(strict=True)
        login = args['login']
        abort_if_user_already_exist(login)
        try:
            id = getFirstMissingID(USERS)
            print(id)
            login = args['login']
            password = args['password']
            user = {}
            user['id'] = id
            user['login'] = login
            user['password'] = password
            USERS.insert(id, user)
            return return_message(user, 201)
        except:
            return_message({},400)

def get_logins():
    return list(map(lambda user: user['login'], USERS))
    
def abort_if_user_already_exist(user_login):
    user_logins = get_logins()
    if user_login in user_logins:
        return_message({},404," User with login {} already exists".format(user_login))

