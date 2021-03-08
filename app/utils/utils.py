from flask import request
from flask_restful import Resource, reqparse, abort

from typing import Dict, List, Any

from app.services.todosService import TODOS
from app.services.listsService import LISTS

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

def get_todo(todo_id:int) ->  Dict[str, Any]:
    return list(filter(lambda todo : todo['id']==todo_id, TODOS))[0]


def get_list_ids() -> List[int]:
    return list(map(lambda list: list['id'], LISTS))

def abort_if_list_doesnt_exist(list_id: int):
    list_ids = get_list_ids()
    if list_id not in list_ids:
        abort(404,  message="Cannot find the LIST with id {}".format(list_id))

def get_list_todos_ids(list_id:int)-> List[int]:
    return list(map(lambda list: list['id'], LISTS[list_id]['todos']))


def abort_if_todo_or_list_doesnt_exist(list_id:int, todo_id: int):
    abort_if_list_doesnt_exist(list_id)
    list_todos_ids = get_list_todos_ids(list_id)
    if todo_id not in list_todos_ids:
        abort(404,  message="Cannot find the TODO with id {} in ths LIST with the id {}".format(todo_id,list_id))
