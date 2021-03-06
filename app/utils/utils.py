from flask import request
from flask_restful import Resource, reqparse, abort

from typing import Dict, List, Any

from app.services.listsService import LISTS
from app.services.accountsService import connected_user
import jwt

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

def abort_if_list_doesnt_exist(list_id: int):
    list_ids = get_ids(LISTS)
    if list_id not in list_ids:
        return_message({},404," Cannot find the LIST with id {}".format(list_id))

def get_list_todos_ids(list_id:int)-> List[int]:
    return list(map(lambda list: list['id'], LISTS[list_id]['todos']))

def abort_if_todo_or_list_doesnt_exist(list_id:int, todo_id: int):
    abort_if_list_doesnt_exist(list_id)
    list = get_element_in_dic(list_id,LISTS)
    list_todos_ids = get_ids(list['todos'])
    if todo_id not in list_todos_ids:
        return_message({},404, " Cannot find the TODO with id {} in ths LIST with the id {}".format(todo_id,list_id))

def return_message(data: Dict[str, Any], status:int, message="") -> Dict[str, Any]:
    if status == 404 :
        abort(status, status=status, message="Not found"+message, data=data)
    if status == 401 :
        abort(status, status=status, message="Unauthorized"+message, data=data)
    if status == 400 :
        abort(status, status=status, message="Bad Request"+message, data=data)
    message = {
        200 : "OK"+message,
        202 : "Accepted",
        201 : "Created"
    }
    return {"status": status,
            "message": message[status], 
            "data":data}

def is_connect(token):
    user = jwt.decode(token,'secret',algorithms=['HS256'])
    if not user['login'] == connected_user['login']:
        return_message({},401," You need to be connect to access to this"+user)

