import os

import pytest
from conftest import create_test_user

from dundie.core import add, load, read
from dundie.database import get_session
from dundie.models import Person
from dundie.utils.db import add_person

from .constants import PEOPLE_FILE


@pytest.fixture(scope="function", autouse=True)
def export_variables_for_test(request):
    """Exporta as variáveis de ambiente para os testes"""
    email, password = create_test_user()
    os.environ["DUNDIE_EMAIL"] = email
    os.environ["DUNDIE_PASSWORD"] = password
    yield
    del os.environ["DUNDIE_EMAIL"]
    del os.environ["DUNDIE_PASSWORD"]


@pytest.mark.unit
def test_add_movement():
    with get_session() as session:
        data = {
            "role": "Salesman",
            "dept": "Sales",
            "name": "Joe Doe",
            "email": "joe@doe.com",
        }
        joe, created = add_person(session, Person(**data))
        assert created is True

        data = {
            "role": "Manager",
            "dept": "Management",
            "name": "Jim Doe",
            "email": "jim@doe.com",
        }
        jim, created = add_person(session, Person(**data))
        assert created is True

        session.commit()

        add(-30, email="joe@doe.com")
        add(90, dept="Management")
        session.refresh(joe)
        session.refresh(jim)

        assert joe.balance[0].value == 470
        assert jim.balance[0].value == 190


@pytest.mark.unit
def test_add_balance_for_dept():
    load(PEOPLE_FILE)
    original = read(dept="Sales")

    add(100, dept="Sales")

    modified = read(dept="Sales")
    for index, person in enumerate(modified):
        assert person["balance"] == original[index]["balance"] + 100


@pytest.mark.unit
def test_add_balance_for_person():
    load(PEOPLE_FILE)
    original = read(email="jim@dundlermifflin.com")

    add(-30, email="jim@dundlermifflin.com")

    modified = read(email="jim@dundlermifflin.com")
    for index, person in enumerate(modified):
        assert person["balance"] == original[index]["balance"] - 30
