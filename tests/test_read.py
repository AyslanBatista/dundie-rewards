import os

import pytest
from conftest import create_test_database
from sqlmodel import select

from dundie.core import load, read
from dundie.database import get_session
from dundie.models import Person, User
from dundie.utils.db import add_person

from .constants import PEOPLE_FILE


@pytest.mark.unit
@create_test_database
def test_read_with_query():
    user_test = 1
    session = get_session()

    data = {
        "role": "Salesman",
        "dept": "Sales",
        "name": "Joe Doe",
        "email": "joe@doe.com",
    }
    _, created = add_person(session, Person(**data))
    assert created is True

    data = {
        "role": "Manager",
        "dept": "Management",
        "name": "Jim Doe",
        "email": "jim@doe.com",
    }
    _, created = add_person(session, Person(**data))
    assert created is True

    session.commit()

    response = read()
    assert len(response) == 2 + user_test

    response = read(dept="Management")
    assert len(response) == 1
    assert response[0]["name"] == "Jim Doe"

    response = read(email="joe@doe.com")
    assert len(response) == 1
    assert response[0]["name"] == "Joe Doe"


@pytest.mark.unit
@create_test_database
def test_read_all_data():
    load(PEOPLE_FILE)
    user_test = 1
    result = read()
    assert len(result) == 3 + user_test


@pytest.mark.unit
@create_test_database
def test_read_only_one_dept():
    load(PEOPLE_FILE)
    result = read(dept="Sales")
    assert len(result) == 2


@pytest.mark.unit
@create_test_database
def test_read_only_one_person():
    load(PEOPLE_FILE)
    result = read(email="jim@dundlermifflin.com")
    assert len(result) == 1


@pytest.mark.unit
@create_test_database
def test_read_query_permission_manager():
    load(PEOPLE_FILE)
    email = "schrute@dundlermifflin.com"
    with get_session() as session:
        filtro = session.exec(
            select(Person, User).join(User).where(Person.email == email)
        ).first()
    os.environ["DUNDIE_EMAIL"] = email
    os.environ["DUNDIE_PASSWORD"] = filtro[1].password

    result = read(show=True)

    assert len(result) == 2
    assert result[0]["dept"] == "Sales"


@pytest.mark.unit
@create_test_database
def test_read_negative_with_query():
    with pytest.raises(SystemExit) as e:
        read(email="m@dlin.com")

    assert e.type == SystemExit
    assert e.value.code == 2
