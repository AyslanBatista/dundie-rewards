"""Core module of dundie"""

import os
import sys
from csv import reader
from typing import Any, Dict, List

from sqlmodel import select

from dundie.database import get_session
from dundie.models import Movement, Person
from dundie.settings import DATEFMT
from dundie.utils.db import add_movement, add_person
from dundie.utils.exchange import get_rates
from dundie.utils.log import get_logger
from dundie.utils.login import check_login, console
from dundie.utils.permission import get_user_role_dept, query_permission

log = get_logger()
Query = Dict[str, Any]
ResultDict = List[Dict[str, Any]]


@check_login
def load(filepath: str) -> ResultDict:
    """Loads data from filepath to the database.

    >>> len(load('assets/people.csv'))
    2
    """
    try:
        csv_data = reader(open(filepath))
    except FileNotFoundError as e:
        log.error(str(e))
        raise e

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

        rates = get_rates(currencies)

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
    return return_data


@check_login
def add(value: int, **query: Query):
    """Add value to each record on query"""
    query = {k: v for k, v in query.items() if v is not None}
    people = read(**query)
    try:
        if not people:
            raise RuntimeError(
                f"{list(query.values())}provided was not found in the database"
            )
    except RuntimeError as e:
        console.print(e, style="danger")

    with get_session() as session:
        email = os.getenv("DUNDIE_EMAIL")
        for person in people:
            instance = session.exec(
                select(Person).where(Person.email == person["email"])
            ).first()

            add_movement(session, instance, value, email)
        session.commit()


@check_login
def transfer(value: int, to: str) -> str:
    """Transfer values between users"""
    user = {"email": os.getenv("DUNDIE_EMAIL")}
    people = read(**user)

    if value > people[0]["balance"]:
        console.print(
            "\n❌ [ERROR] Insufficient balance to complete the transfer.\n",
            style="danger",
        )
        sys.exit(1)

    if user["email"] == to:
        console.print(
            "\n❌ [ERROR] You cannot transfer to yourself.\n", style="danger"
        )
        sys.exit(1)

    add_to = {"email": to}
    add(-value, **user)
    add(value, **add_to)

    receiver_name = read(**add_to)
    return receiver_name[0]["name"]


@check_login
def movements():
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
