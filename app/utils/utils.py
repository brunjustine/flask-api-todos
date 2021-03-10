from flask import request
from flask_restful import Resource, reqparse, abort

from typing import Dict, List, Any

from app.services.todosService import TODOS
from app.services.listsService import LISTS

def get_ids(DICO : Dict[str, Any]) -> List[int]:
    return list(map(lambda e: e['id'], DICO))

def getFirstMissingID(DICO : Dict[str, Any]) -> int:
    ids = get_ids(DICO)
    i = 1
    while (i < len(ids)):
        if (DICO[i-1]['id'] == DICO[i]['id'] - 1):
            i+=1
        else:
            break
    return i

def get_element_in_dic(id : int , dico : Dict[str, Any]) ->Dict[str, Any] :
    return list(filter(lambda e : e['id']==id, dico))[0]

def get_all_todos() -> Dict[str, Any] :
    return list(map(lambda list: list['todos'], LISTS))

# TODELETE
def abort_if_todo_doesnt_exist(todo_id: int):
    todo_ids = get_ids(TODOS)
    if todo_id not in todo_ids:
        abort(404,  message="Cannot find the TODO with id {}".format(todo_id))

# TODELETE
def abort_if_todo_already_exist(todo_id: int):
    todo_ids = get_ids(TODOS)
    if todo_id in todo_ids:
        abort(404,  message="TODO with id {} already exists".format(todo_id))

# TODELETE
def abort_if_todo_has_negative_id(todo_id: int):
    if todo_id < 0:
        abort(404,  message="TODO cannot have negative id value")

# TODELETE
def get_todo(todo_id:int) ->  Dict[str, Any]:
    return list(filter(lambda todo : todo['id']==todo_id, TODOS))[0]

def abort_if_list_doesnt_exist(list_id: int):
    list_ids = get_ids(LISTS)
    if list_id not in list_ids:
        abort(404,  message="Cannot find the LIST with id {}".format(list_id))

def get_list_todos_ids(list_id:int)-> List[int]:
    return list(map(lambda list: list['id'], LISTS[list_id]['todos']))

def abort_if_todo_or_list_doesnt_exist(list_id:int, todo_id: int):
    abort_if_list_doesnt_exist(list_id)
    list = get_element_in_dic(list_id,LISTS)
    list_todos_ids = get_ids(list['todos'])
    if todo_id not in list_todos_ids:
        abort(404,  message="Cannot find the TODO with id {} in ths LIST with the id {}".format(todo_id,list_id))

def return_message(data: Dict[str, Any], status:int) -> Dict[str, Any]:
    message = {
        200 : "OK",
        201 : "Created",
        400 : "Bad Request",
        404 : "Not found"
    }
    return {"status": status,
            "message": message[status], 
            "data":data}