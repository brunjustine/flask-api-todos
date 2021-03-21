from app import api

from app.resources.login import LoginResource
from app.resources.accounts import AccountsManagementResource
from app.resources.lists import ListManagementResource, ListTodoManagementResourceByID, ListManagementResourceByID, ListTodosManagementResourceByID

# Login
api.add_resource(LoginResource, '/api/login')

#Authentification
api.add_resource(AccountsManagementResource, '/api/account')

#List app
api.add_resource(ListManagementResource, '/api/lists')
api.add_resource(ListManagementResourceByID, '/api/lists/<int:list_id>')
api.add_resource(ListTodosManagementResourceByID, '/api/lists/todos/<int:list_id>')
api.add_resource(ListTodoManagementResourceByID, '/api/lists/todos/<int:list_id>/<int:todo_id>')
