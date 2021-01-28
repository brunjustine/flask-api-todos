from app import api

from app.resources.helloworld import HelloWorldResource, HelloWorldResourceNameToken, HelloWorldResourceNameURL, HelloWorldResourceNames
from app.resources.login import LoginResource
from app.resources.todos import TodoManagementResource, TodoManagementResourceByID
from app.resources.lists import ListManagementResource, ListTodoManagementResourceByID, ListManagementResourceByID, ListTodosManagementResourceByID

# Hello World
api.add_resource(HelloWorldResource, '/api/helloworld')
api.add_resource(HelloWorldResourceNameToken, '/api/hello')
api.add_resource(HelloWorldResourceNameURL, '/api/hello/<string:name>')
api.add_resource(HelloWorldResourceNames, '/api/hello/<int:count>')

# Login
api.add_resource(LoginResource, '/api/login')

# Todos app
api.add_resource(TodoManagementResource, '/api/todos')
api.add_resource(TodoManagementResourceByID, '/api/todos/<int:todo_id>')

#List app
api.add_resource(ListManagementResource, '/api/lists')
api.add_resource(ListManagementResourceByID, '/api/lists/<int:list_id>')
api.add_resource(ListTodosManagementResourceByID, '/api/lists/todos/<int:list_id>')
api.add_resource(ListTodoManagementResourceByID, '/api/lists/todos/<int:list_id>/<int:todo_id>')
