import os

import pytest
from conftest import create_test_database
from sqlmodel import select

from dundie.core import load
from dundie.database import get_session
from dundie.models import Person, User
from dundie.utils.permission import (
    check_permission_ceo,
    filter_data,
    get_user_role_dept,
)

from .constants import PEOPLE_FILE


@pytest.mark.unit
@create_test_database
def test_permission_and_filter_data_positive_CEO():
    user = get_user_role_dept()

    @check_permission_ceo
    def my_function():
        return "Original function performed"

    result = my_function()
    filter_data_ceo = filter_data(user)

    assert result == "Original function performed"
    assert filter_data_ceo == []


@pytest.mark.unit
@create_test_database
def test_filter_data_positive_employee():
    load(PEOPLE_FILE)

    email = "jim@dundlermifflin.com"
    with get_session() as session:
        filtro = session.exec(
            select(Person, User).join(User).where(Person.email == email)
        ).first()
    os.environ["DUNDIE_EMAIL"] = email
    os.environ["DUNDIE_PASSWORD"] = filtro[1].password

    user = get_user_role_dept()
    filter_data_employee = filter_data(user)

    with get_session() as session:
        sql = session.exec(select(Person).where(*filter_data_employee))

        result = list(sql)

    assert result[0].email == email
    assert result[0].dept == user["dept"]


@pytest.mark.unit
@create_test_database
def test_permission_negative_permission_denied():
    load(PEOPLE_FILE)

    email = "jim@dundlermifflin.com"
    with get_session() as session:
        filtro = session.exec(
            select(Person, User).join(User).where(Person.email == email)
        ).first()
    os.environ["DUNDIE_EMAIL"] = email
    os.environ["DUNDIE_PASSWORD"] = filtro[1].password

    with pytest.raises(SystemExit) as e:

        @check_permission_ceo
        def my_function():
            return "Original function performed"

        my_function()

    assert e.type == SystemExit
    assert e.value.code == 6
