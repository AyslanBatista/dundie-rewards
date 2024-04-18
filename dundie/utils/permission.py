import os
from functools import wraps
from typing import Any, Dict

from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person

Query = Dict[str, Any]


class PermissionDenied(Exception):
    """
    Exceção personalizada para erros de autenticação.
    """

    def __init__(self, message):
        self.message = message


def get_user_role_dept():
    """Obtaining the role,department and email
    information of the user connected to the system"""
    user_role_dept = {"role": None, "dept": None, "email": None}
    user = os.getenv("DUNDIE_USER")
    user_role_dept["email"] = user
    with get_session() as session:
        instance = session.exec(
            select(Person).where(Person.email == user)
        ).first()
        user_role_dept["role"] = instance.role
        user_role_dept["dept"] = instance.dept

    return user_role_dept


def filter_data(role_dpt: dict) -> str:
    """creating a filter based on user permission"""
    filter_ = []
    if role_dpt["role"] == "Manager":
        filter_.append(Person.dept == role_dpt["dept"])
        return filter_
    if role_dpt["role"] == "CEO":
        return []
    else:
        filter_.append(Person.email == role_dpt["email"])
        return filter_


def query_permission(sql: Query) -> Query:
    """Receiving a sql and returning with a where
    application based on the permission the user has"""
    user_role_dept = get_user_role_dept()
    filter_permission = filter_data(user_role_dept)
    if filter_permission:
        sql = sql.where(*filter_permission)
    return sql


def check_permission_ceo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Função para obter a função do usuário atual
        user_role_dept = get_user_role_dept()
        if user_role_dept["role"] == "CEO":
            return func(*args, **kwargs)
        else:
            raise PermissionDenied(
                "❌ [ERROR] You do not have permission to run this command"
            )

    return wrapper
