from flask import request
from flask_restful import Resource, reqparse, abort

from typing import Dict, List, Any

from app.services.listsService import LISTS
from app.services.todosService import TODOS

from app.utils.utils import *

class ListManagementResource(Resource):
    def get(self) -> Dict[str,Any]:
        """
        Return all the LISTS contained in the lists service
        ---
        tags:
            - Flask API
        responses:
            200:
                description: JSON representing all the elements of the lists service    
        """
        return LISTS,200


class ListManagementResourceByTodoID(Resource):
     def get(self, list_id: int, todo_id: int) -> Dict[str, Any]:
        """
        Get the content of a todo of a list in the lists service
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: list_id
              description: The id of the list to get
              required: true
              type: string
            - in: path
              name : todo_id
              description: The id of the todo to get
              required: true
              type: string
        responses:
            200:
                description: JSON representing the todo
            404:
                description: The todo or the list does not exist
        """
        abort_if_todo_or_list_doesnt_exist(list_id,todo_id)
        try : 
            todos =  LISTS[list_id]
            todo = todos['list'][todo_id]
            return todo, 200
        except:
            abort(400)

class ListManagementResourceByID(Resource):
    def get(self, list_id: int) -> Dict[str, Any]:
        """
        Get the content of a list in the lists service
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: list_id
              description: The id of the list to get
              required: true
              type: string
        responses:
            200:
                description: JSON representing the list
            404:
                description: The list does not exist
        """
        abort_if_list_doesnt_exist(list_id)
        return LISTS[list_id], 200

