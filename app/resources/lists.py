from flask import request
from flask_restful import Resource, reqparse, abort

from typing import Dict, List, Any

from app.services.listsService import LISTS
from app.services.todosService import TODOS

from app.utils.utils import *


class ListManagementResource(Resource):
    def get(self) -> Dict[str, Any]:
        """
        Return all the LISTS contained in the lists service
        ---
        tags:
            - Flask API
        responses:
            200:
                description: JSON representing all the elements of the lists service
        """
        body_parser = reqparse.RequestParser(bundle_errors=True)  # Throw all the elements that has been filled uncorrectly
        body_parser.add_argument('token', location='headers', required=True)
        args = body_parser.parse_args(strict=True)
        try:
            is_connect(args['token'])
        except:
            return_message({},401)
        return return_message(LISTS, 200)


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
        body_parser = reqparse.RequestParser(
            bundle_errors=True)  # Throw all the elements that has been filled uncorrectly
        body_parser.add_argument(
            'name', type=str, required=True, help="Missing the name of the list")
        body_parser.add_argument(
            'created_on', type=str, required=True, help="Missing the creation date of the list")
        body_parser.add_argument('token', location='headers', required=True)
        # Accepted only if these two parameters are strictly declared in body else raise exception
        args = body_parser.parse_args(strict=True)
        try:
            is_connect(args['token'])
        except:
            return_message({},401)
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
            return return_message(list, 201)
        except:
            return_message({},400)


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
        body_parser = reqparse.RequestParser(bundle_errors=True)  # Throw all the elements that has been filled uncorrectly
        body_parser.add_argument('token', location='headers', required=True)
        args = body_parser.parse_args(strict=True)
        try:
            is_connect(args['token'])
        except:
            return_message({},401)
        abort_if_list_doesnt_exist(list_id)
        return return_message(get_element_in_dic(list_id, LISTS), 200)

    def delete(self, list_id: int) -> Dict[str, Any]:
        """
        Delete the content of a list in the list service
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: list_id
              description: The id of the list to delete
              required: true
              type: string
        responses:
            200:
                description: JSON representing the lists
            404:
                description: The list does not exist
        """
        body_parser = reqparse.RequestParser(bundle_errors=True)  # Throw all the elements that has been filled uncorrectly
        body_parser.add_argument('token', location='headers', required=True)
        args = body_parser.parse_args(strict=True)
        try:
            is_connect(args['token'])
        except:
            return_message({},401)
        abort_if_list_doesnt_exist(list_id)
        list = get_element_in_dic(list_id, LISTS)
        LISTS.remove(list)
        return return_message(list, 200)

    def patch(self, list_id: int) -> Dict[str, Any]:
        """
        Update the content of a list in the list service
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: list_id
              description: The id of the list to update
              required: true
              type: string
            - in: body
              name: attributes
              description: The updated name and/or the creation date of the list
              schema:
                type: object
                properties:
                  name:
                    type: string
                  created_on:
                    type: string
        responses:
            202:
                description: JSON representing updated list if new data has been given by the body
            400:
                description: The parameters are missing or are not correct
            404:
                description: The list does not exist
        """        
        
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('token', location='headers', required=True)
        body_parser.add_argument(
            'name', type=str, required=False, help="Missing the name of the list")
        body_parser.add_argument(
            'created_on', type=str, required=False, help="Missing the creation date of the list")
        args = body_parser.parse_args(strict=False)
        abort_if_list_doesnt_exist(list_id)
        try:
            is_connect(args['token'])
        except:
            return_message({},401)
        try:
            list = get_element_in_dic(list_id, LISTS)
            name = args['name']
            created_on = args['created_on']
            if name != None:
                list['name'] = name
            if created_on != None:
                list['created_on'] = created_on
            list_to_update = get_element_in_dic(list_id, LISTS)
            list_to_update = list
            # Accepted, updated or not if putting the same data
            return return_message(list_to_update, 202)
        except:
            return_message({},400)


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
        body_parser = reqparse.RequestParser(bundle_errors=True)  # Throw all the elements that has been filled uncorrectly
        body_parser.add_argument('token', location='headers', required=True)
        args = body_parser.parse_args(strict=True)
        try:
            is_connect(args['token'])
        except:
            return_message({},401)
        abort_if_list_doesnt_exist(list_id)
        try:
            list = get_element_in_dic(list_id, LISTS)
            todos = list['todos']
            return return_message(todos, 200)
        except:
            return_message({},400)

    def put(self, list_id: int) -> Dict[str, Any]:
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
        # Throw all the elements that has been filled uncorrectly
        body_parser = reqparse.RequestParser(bundle_errors=True)
        body_parser.add_argument(
            'token', location='headers', required=True)
        body_parser.add_argument(
            'name', type=str, required=True, help="Missing the name of the task")
        body_parser.add_argument(
            'created_on', type=str, required=True, help="Missing the creation date of the task")
        body_parser.add_argument(
            'description', type=str, required=False, help="Missing the description of the task")
        # Accepted only if these two parameters are strictly declared in body else raise exception
        args = body_parser.parse_args(strict=True)
        try:
            is_connect(args['token'])
        except:
            return_message({},401)
        abort_if_list_doesnt_exist(list_id)
        try:
            list = get_element_in_dic(list_id, LISTS)
            id = getFirstMissingID(list['todos'])
            print(id)
            name = args['name']
            created_on = args['created_on']
            description = args['description']
            todo = {}
            todo['id'] = id
            task = {} 
            task['name'] = name
            task['created_on'] = created_on
            if description != None:
                task['description'] = description
            todo['task'] = task  
            list['todos'].insert(id, todo)
            return return_message(list, 201)
        except:
            return_message({},400)


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
        body_parser = reqparse.RequestParser(bundle_errors=True)  # Throw all the elements that has been filled uncorrectly
        body_parser.add_argument('token', location='headers', required=True)
        args = body_parser.parse_args(strict=True)
        try:
            is_connect(args['token'])
        except:
            return_message({},401)
        abort_if_todo_or_list_doesnt_exist(list_id, todo_id)
        try:
            list = get_element_in_dic(list_id, LISTS)
            todos = list['todos']
            todo_by_ID = get_element_in_dic(todo_id, todos)
            return return_message(todo_by_ID, 200)
        except:
            return_message({},400)

    def delete(self, list_id: int, todo_id: int) -> Dict[str, Any]:
        """
        Delete the content of a todo of a list in the list service
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: todo_id
              description: The id of the list to delete
              required: true
              type: string
        responses:
            200:
                description: JSON representing the lists
            404:
                description: The list does not exist
        """
        body_parser = reqparse.RequestParser(bundle_errors=True)  # Throw all the elements that has been filled uncorrectly
        body_parser.add_argument('token', location='headers', required=True)
        args = body_parser.parse_args(strict=True)
        try:
            is_connect(args['token'])
        except:
            return_message({},401)
        abort_if_todo_or_list_doesnt_exist(list_id, todo_id)
        list = get_element_in_dic(list_id, LISTS)
        todo = get_element_in_dic(todo_id, list['todos'])
        list['todos'].remove(todo)
        return return_message(todo, 200)

    def patch(self, list_id: int, todo_id: int) -> Dict[str, Any]:
        """
        Update the content of a todo of a list in the list service
        ---
        tags:
            - Flask APIn
        parameters:
            - in: path
                name: list_id
                description: The id of the list of the todo to update
                required: true
                type: string
                - in: path
                name: todo_id
                description: The id of the todo to update
                required: true
                type: string
            - in: body
                name: attributes
                description: The updated name and/or the creation date of the todo of a list
                schema:
                type: object
                properties:
                    name:
                    type: string
                    created_on:
                    type: string
        responses:
            202:
                description: JSON representing updated list and todo if new data has been given by the body
            400:
                description: The parameters are missing or are not correct
            404:
                description: The list or the todo does not exist 
        """        
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('token', location='headers', required=True)
        body_parser.add_argument('name', type=str, required=False, help="Missing the name of the todo")
        body_parser.add_argument('created_on', type=str, required=False, help="Missing the creation date of the todo")
        body_parser.add_argument('description', type=str, required=False, help="Missing the description of the todo")
        args = body_parser.parse_args(strict=True)
        abort_if_todo_or_list_doesnt_exist(list_id, todo_id)
        try:
            is_connect(args['token'])
        except:
            return_message({},401)
        try:
            list = get_element_in_dic(list_id, LISTS)
            todo = get_element_in_dic(todo_id, list['todos'])
            name = args['name']
            created_on = args['created_on']
            description = args['description']
            if name != None:
                todo['task']['name'] = name
            if created_on != None:
                todo['task']['created_on'] = created_on
            if description != None:
                todo['task']['description'] = description
            todo_to_update = get_element_in_dic(todo_id, list['todos'])
            todo_to_update = todo
            return return_message(todo_to_update, 202)  # Accepted, updated or not if putting the same data
        except:
            return_message({},400)
