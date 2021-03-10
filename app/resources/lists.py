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
        return return_message(LISTS,200)
        
    def put(self) -> Dict[str, Any]:
        """
        Create the content of a list in the lists service
        ---
        tags:
            - Flask API
        parameters:
            - in: body
              name: attributes
              description: The name and creation date of the task to create
              schema:
                type: object
                required:
                    - name
                    - created_on
                properties:
                  name:
                    type: string
                  created_on:
                    type: string
        responses:
            201:
                description: JSON representing created list
            400:
                description: The parameters are missing or are not correct
        """
        body_parser = reqparse.RequestParser(bundle_errors=True) # Throw all the elements that has been filled uncorrectly
        body_parser.add_argument('name', type=str, required=True, help="Missing the name of the list")
        body_parser.add_argument('created_on', type=str, required=True, help="Missing the creation date of the list")
        args = body_parser.parse_args(strict=True) # Accepted only if these two parameters are strictly declared in body else raise exception
        try:
            id = getFirstMissingID(LISTS)
            print(id)
            name = args['name']
            created_on = args['created_on']
            list = {}
            list['id'] = id
            list['name'] = name
            list['created_on'] = created_on
            list['todos'] = []
            LISTS.insert(id, list)
            return return_message(list,201)
        except:
            abort(400,return_message({},400))
            


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
        return return_message(get_element_in_dic(list_id,LISTS), 200)

class ListTodosManagementResourceByID(Resource):
    def get(self, list_id: int) -> Dict[str, Any]:
        """
        Get the todos of a list in the lists service
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: list_id
              description: The id of the list to get the todos
              required: true
              type: string
        responses:
            200:
                description: JSON representing the list
            404:
                description: The list does not exist
        """
        abort_if_list_doesnt_exist(list_id)
        try : 
            list = get_element_in_dic(list_id,LISTS)
            todos =  list['todos']
            return return_message(todos, 200)
        except:
            abort(400,return_message({},400))

    def put(self, list_id:int) -> Dict[str, Any]:
        """
        Create the content of a todo in a list in the lists service
        ---
        tags:
            - Flask API
        parameters:
            - in: body
            name: attributes
            description: The name and creation date of the task to create
            schema:
                type: object
                required:
                    - name
                    - created_on
                properties:
                name:
                    type: string
                created_on:
                    type: string
        responses:
            201:
                description: JSON representing created todo in the list
            400:
                description: The parameters are missing or are not correct
        """
        abort_if_list_doesnt_exist(list_id)
        # Throw all the elements that has been filled uncorrectly
        body_parser = reqparse.RequestParser(bundle_errors=True)
        body_parser.add_argument(
            'name', type=str, required=True, help="Missing the name of the task")
        body_parser.add_argument(
            'created_on', type=str, required=True, help="Missing the creation date of the task")
        # Accepted only if these two parameters are strictly declared in body else raise exception
        args = body_parser.parse_args(strict=True)
        try:
            id = getFirstMissingID(TODOS)
            print(id)
            name = args['name']
            created_on = args['created_on']
            todo = {}
            todo['id'] = id
            todo['name'] = name
            todo['created_on'] = created_on
            list = get_element_in_dic(list_id, LISTS)
            list['todos'].insert(id,todo)
            return return_message(list, 201)
        except:
            abort(400, test=return_message({},400))

class ListTodoManagementResourceByID(Resource):
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
            list = get_element_in_dic(list_id,LISTS)
            todos = list['todos']
            todo_by_ID = get_element_in_dic(todo_id,todos)
            return return_message(todo_by_ID, 200)
        except:
            abort(400,return_message({},400))

