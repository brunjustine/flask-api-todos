from flask import request
from flask_restful import Resource, reqparse, abort

from typing import Dict, List, Any

from app.services.todosService import TODOS

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
        return TODOS, 200

    def put(self) -> Dict[str, Any]:
        """
        Create the content of a todo in the todos service
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
                description: JSON representing created todo
            400:
                description: The parameters are missing or are not correct
        """
        body_parser = reqparse.RequestParser(bundle_errors=True) # Throw all the elements that has been filled uncorrectly
        body_parser.add_argument('name', type=str, required=True, help="Missing the name of the task")
        body_parser.add_argument('created_on', type=str, required=True, help="Missing the creation date of the task")
        args = body_parser.parse_args(strict=True) # Accepted only if these two parameters are strictly declared in body else raise exception
        try:
            id = getFirstMissingID()
            print(id)
            name = args['name']
            created_on = args['created_on']
            todo = {}
            todo['id'] = id
            todo['task'] = {'name':name, 'created_on':created_on}
            TODOS.insert(id, todo)
            return todo, 201
        except:
            abort(400)

class TodoManagementResourceByID(Resource):

    def get(self, todo_id: int) -> Dict[str, Any]:
        """
        Get the content of a todo in the todos service
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: todo_id
              description: The id of the todo to get
              required: true
              type: string
        responses:
            200:
                description: JSON representing the todo
            404:
                description: The todo does not exist
        """
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id], 200

    def delete(self, todo_id: int) -> Dict[str, Any]:
        """
        Delete the content of a todo in the todos service
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: todo_id
              description: The id of the todo to delete
              required: true
              type: string
        responses:
            200:
                description: JSON representing the todos
            404:
                description: The todo does not exist
        """
        abort_if_todo_doesnt_exist(todo_id)
        todo = TODOS[:][todo_id]
        del TODOS[todo_id]
        return todo, 200

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
            task = TODOS[todo_id]
            name = args['name']
            created_on = args['created_on']
            if name != None:
                task['task']['name'] = name
            if created_on != None:
                task['task']['created_on'] = created_on
            TODOS[todo_id] = task
            return task, 202 # Accepted, updated or not if putting the same data
        except:
            abort(400)

def get_todo_ids() -> List[int]:
    return list(map(lambda todo: todo['id'], TODOS))

def abort_if_todo_doesnt_exist(todo_id: int):
    todo_ids = get_todo_ids()
    if todo_id not in todo_ids:
        abort(404,  message="Cannot find the TODO with id {}".format(todo_id))

def abort_if_todo_already_exist(todo_id: int):
    todo_ids = get_todo_ids()
    if todo_id in todo_ids:
        abort(404,  message="TODO with id {} already exists".format(todo_id))

def abort_if_todo_has_negative_id(todo_id: int):
    if todo_id < 0:
        abort(404,  message="TODO cannot have negative id value")

def getFirstMissingID() -> int:
    todo_ids = get_todo_ids()
    i = 1
    while (i < len(todo_ids)):
        if (TODOS[i-1]['id'] == TODOS[i]['id'] - 1):
            i+=1
        else:
            break
    return i
