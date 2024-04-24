import os

import pytest
from conftest import create_test_database
from sqlmodel import select

from dundie.core import load, read, transfer
from dundie.database import get_session
from dundie.models import Movement, Person

from .constants import PEOPLE_FILE


@pytest.mark.unit
@create_test_database
def test_transfer_positive_query_email():
    load(PEOPLE_FILE)
    original_user = read(email=os.getenv("DUNDIE_EMAIL"))
    original_sender = read(email="jim@dundlermifflin.com")

    transfer(value=100, email="jim@dundlermifflin.com")

    modified_user = read(email=os.getenv("DUNDIE_EMAIL"))
    modified_sender = read(email="jim@dundlermifflin.com")

    assert modified_sender[0]["balance"] == original_sender[0]["balance"] + 100
    assert modified_user[0]["balance"] == original_user[0]["balance"] - 100


@pytest.mark.unit
@create_test_database
def test_transfer_negative_query_email_yourself():
    load(PEOPLE_FILE)
    user = os.getenv("DUNDIE_EMAIL")
    with pytest.raises(SystemExit) as e:
        transfer(value=100, email=user)

    assert e.type == SystemExit
    assert 7 == e.value.code


@pytest.mark.unit
@create_test_database
def test_transfer_positive_query_dept():
    load(PEOPLE_FILE)
    original_user = read(email=os.getenv("DUNDIE_EMAIL"))
    original_sender = read(dept="Sales")

    transfer(value=100, dept="Sales")

    modified_user = read(email=os.getenv("DUNDIE_EMAIL"))
    modified_sender = read(dept="Sales")

    assert modified_user[0]["balance"] == (
        original_user[0]["balance"] - 100 * len(modified_sender)
    )
    for index, person in enumerate(modified_sender):
        assert person["balance"] == original_sender[index]["balance"] + 100


@pytest.mark.unit
@create_test_database
def test_transfer_negative_insufficient_balance():
    load(PEOPLE_FILE)
    with pytest.raises(SystemExit) as e:
        transfer(value=300, dept="Sales")

    assert e.type == SystemExit
    assert 3 == e.value.code


@pytest.mark.unit
@create_test_database
def test_transfer_positive_movement_query_email():
    load(PEOPLE_FILE)
    user_email = os.getenv("DUNDIE_EMAIL")
    transfer(value=100, email="jim@dundlermifflin.com")

    with get_session() as session:
        user = session.exec(
            select(Person).where(Person.email == user_email)
        ).first()

        sender = session.exec(
            select(Person).where(Person.email == "jim@dundlermifflin.com")
        ).first()

        movement_user = session.exec(
            select(Movement).where(Movement.person_id == user.id)
        )
        list_user = list(movement_user)
        movement_sender = session.exec(
            select(Movement).where(Movement.person_id == sender.id)
        )
        list_sender = list(movement_sender)

    assert list_user[-1].value == -100
    assert list_user[-1].actor == user.email

    assert list_sender[-1].value == 100
    assert list_sender[-1].actor == user.email


@pytest.mark.unit
@create_test_database
def test_transfer_positive_movement_query_dept():
    load(PEOPLE_FILE)
    user_email = os.getenv("DUNDIE_EMAIL")
    transfer(value=100, dept="Sales")

    with get_session() as session:
        user = session.exec(
            select(Person).where(Person.email == user_email)
        ).first()
        movement_user = session.exec(
            select(Movement).where(Movement.person_id == user.id)
        )
        list_user = list(movement_user)

        senders = session.exec(select(Person).where(Person.dept == "Sales"))

        list_senders = []
        for sender in senders:

            movement_sender = session.exec(
                select(Movement).where(Movement.person_id == sender.id)
            )
            list_senders.append(list(movement_sender))

    assert list_user[-1].value == -200
    assert list_user[-1].actor == user.email

    assert list_senders[0][-1].value == 100
    assert list_senders[0][-1].actor == user.email
    assert list_senders[1][-1].value == 100
    assert list_senders[1][-1].actor == user.email
