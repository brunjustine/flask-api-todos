from flask import request
from flask_restful import Resource, reqparse, abort

from typing import Dict, List, Any

from app.services.todosService import TODOS
from app.utils.utils import *

class TodoManagementResource(Resource):

    def get(self) -> Dict[str, Any]:
        """
        Return all the TODOS contained in the todos service
        ---
        tags:
            - Flask API
        responses:
            200:
                description: JSON representing all the elements of the todos service
        """
        todos = get_all_todos()
        return return_message(todos, 200)

class TodoManagementResourceByID(Resource):
    def patch(self, todo_id: int) -> Dict[str, Any]:
        """
        Create the content of a todo in the todos service
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: todo_id
              description: The id of the todo to update
              required: true
              type: string
            - in: body
              name: attributes
              description: The updated name and/or the creation date of the task
              schema:
                type: object
                properties:
                  name:
                    type: string
                  created_on:
                    type: string
        responses:
            202:
                description: JSON representing updated todo if new data has been given by the body
            400:
                description: The parameters are missing or are not correct
            404:
                description: The todo does not exist
        """
        abort_if_todo_doesnt_exist(todo_id)
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('name', type=str, required=False, help="Missing the name of the task")
        body_parser.add_argument('created_on', type=str, required=False, help="Missing the creation date of the task")
        args = body_parser.parse_args(strict=False)
        try:
            task = get_element_in_dic(todo_id,TODOS)
            name = args['name']
            created_on = args['created_on']
            if name != None:
                task['task']['name'] = name
            if created_on != None:
                task['task']['created_on'] = created_on
            todo_to_update = get_element_in_dic(todo_id,TODOS)
            todo_to_update = task
            return return_message(task, 202) # Accepted, updated or not if putting the same data
        except:
            abort(400,return_message({},400))

