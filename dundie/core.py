"""Core module of dundie"""

import json
import os
import sys
from csv import reader
from typing import Any, Dict, List

from sqlmodel import select

from dundie.database import get_session
from dundie.models import Movement, Person
from dundie.settings import API_BASE_URL, DATEFMT
from dundie.utils.db import add_movement, add_person
from dundie.utils.exchange import get_rates
from dundie.utils.json_serealizer import DecimalEncoder
from dundie.utils.log import log
from dundie.utils.login import check_login, console
from dundie.utils.permission import (
    check_permission_ceo,
    get_user_role_dept,
    query_permission,
)

Query = Dict[str, Any]
ResultDict = List[Dict[str, Any]]


class InvalidBeneficiaryError(Exception):
    pass


class InsufficientBalanceError(Exception):
    pass


@check_login
@check_permission_ceo
def load(filepath: str) -> ResultDict:
    """Loads data from filepath to the database.

    >>> len(load('assets/people.csv'))
    2
    """
    try:
        csv_data = reader(open(filepath))
    except FileNotFoundError as e:
        log.error(str(e))
        console.print(e, style="danger")
        sys.exit(1)

    people = []
    headers = ["name", "dept", "role", "email", "currency"]

    with get_session() as session:
        for line in csv_data:
            person_data = dict(zip(headers, [item.strip() for item in line]))
            instance = Person(**person_data)
            person, created = add_person(session, instance)
            return_data = person.dict(exclude={"id"})
            return_data["created"] = created
            people.append(return_data)

        session.commit()
    return people


@check_login
def read(show=False, **query: Query) -> ResultDict:
    """Read data from db and filters using query

    read(email="joe@doe.com")
    """
    query = {k: v for k, v in query.items() if v is not None}
    return_data = []
    query_statements = []
    if "dept" in query:
        query_statements.append(Person.dept == query["dept"])
    if "email" in query:
        query_statements.append(Person.email == query["email"])
    sql = select(Person)
    if query_statements:
        sql = sql.where(*query_statements)

    if show:
        sql = query_permission(sql)

    with get_session() as session:
        currencies = session.exec(
            select(Person.currency).distinct(Person.currency)
        )

        rates = get_rates(currencies=currencies, url=API_BASE_URL)

        results = session.exec(sql)
        for person in results:
            total = rates[person.currency].value * person.balance[0].value
            return_data.append(
                {
                    "name": person.name,
                    "email": person.email,
                    "dept": person.dept,
                    "role": person.role,
                    "balance": person.balance[0].value,
                    "last_movement": person.movement[-1].date.strftime(
                        DATEFMT
                    ),
                    "currency": person.currency,
                    **{"value": total},
                }
            )
    try:
        if not return_data:
            raise RuntimeError(
                f"{list(query.values())}provided was not found in the database"
            )
    except RuntimeError as e:
        log.error(e)
        console.print(e, style="danger")
        sys.exit(2)
    return return_data


@check_login
@check_permission_ceo
def add(value: int, **query: Query):
    """Add value to each record on query"""
    query = {k: v for k, v in query.items() if v is not None}
    people = read(**query)

    with get_session() as session:
        email = os.getenv("DUNDIE_EMAIL")
        for person in people:
            instance = session.exec(
                select(Person).where(Person.email == person["email"])
            ).first()

            add_movement(session, instance, value, email)
        session.commit()


@check_login
def transfer(value: int, **to: Query) -> tuple[int, list]:
    """Transfer values between users"""
    query = {k: v for k, v in to.items() if v is not None}
    data_people = read(**query)

    user = {"email": os.getenv("DUNDIE_EMAIL")}
    data_user = read(**user)
    removed_value = value * len(data_people)
    try:
        if user["email"] == data_people[0]["email"]:
            raise InvalidBeneficiaryError(
                "\n❌ [ERROR] You cannot transfer to yourself.\n"
            )

        if removed_value > data_user[0]["balance"]:
            raise InsufficientBalanceError(
                "\n❌ [ERROR] Insufficient balance to complete the transfer.\n"
            )

    except InsufficientBalanceError as e:
        log.error(str(e).strip())
        console.print(e, style="danger")
        sys.exit(3)

    except InvalidBeneficiaryError as e:
        log.error(str(e).strip())
        console.print(e, style="danger")
        sys.exit(7)

    with get_session() as session:
        email = os.getenv("DUNDIE_EMAIL")
        instance_user = session.exec(
            select(Person).where(Person.email == data_user[0]["email"])
        ).first()
        add_movement(session, instance_user, -removed_value, email)

        for person in data_people:
            instance = session.exec(
                select(Person).where(Person.email == person["email"])
            ).first()

            add_movement(session, instance, value, email)
        session.commit()

    return removed_value, data_people


@check_login
def movements():
    """returns the movement data of the user that was informed"""
    return_data = []
    user = get_user_role_dept()
    with get_session() as session:

        instance_id = session.exec(
            select(Person).where(Person.email == user["email"])
        ).first()
        user_id = instance_id.id

        instance_movements = session.exec(
            select(Movement).where(Movement.person_id == user_id)
        )

        for movement in instance_movements:
            return_data.append(
                {
                    "date": movement.date.strftime(DATEFMT),
                    "value": movement.value,
                    "user": movement.actor,
                }
            )
    return return_data


def generating_json_file(data: str, path: str):
    """Generating a json file with the data and path provided"""
    try:
        with open(path, "w") as path_file:
            path_file.write(json.dumps(data, cls=DecimalEncoder))
        console.print(
            f"📄 [bold green]Success![/] File with the desired"
            f" information was saved in {path!r}.\n",
            style="info",
        )
    except PermissionError as e:
        log.error(str(e))
        console.print(e, style="danger")
        sys.exit(4)
