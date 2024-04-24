import os

import pytest
from conftest import create_test_database
from sqlmodel import select

from dundie.core import load, movements, transfer
from dundie.database import get_session
from dundie.models import Movement, Person

from .constants import PEOPLE_FILE


@pytest.mark.unit
@create_test_database
def test_movements_positive():
    load(PEOPLE_FILE)
    transfer(value=100, dept="Sales")
    transfer(value=100, dept="Directory")

    with get_session() as session:
        user = session.exec(
            select(Person).where(Person.email == os.getenv("DUNDIE_EMAIL"))
        ).first()
        movement_user = session.exec(
            select(Movement).where(Movement.person_id == user.id)
        )
        list_user = list(movement_user)

    data = movements()

    assert len(data) == len(list_user)
    assert data[-1]["value"] == list_user[-1].value
