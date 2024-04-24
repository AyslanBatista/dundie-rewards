import pytest
from conftest import create_test_database, create_test_user
from sqlmodel import select

from dundie.core import load
from dundie.database import get_session
from dundie.models import Person
from dundie.settings import API_BASE_URL
from dundie.utils.exchange import get_rates

from .constants import PEOPLE_FILE


@pytest.mark.unit
@create_test_database
def test_exchange_positive():
    load(PEOPLE_FILE)
    with get_session() as session:
        currencies = session.exec(
            select(Person.currency).distinct(Person.currency)
        )
        data = get_rates(currencies, url=API_BASE_URL)

    assert len(data) == 2
    assert data["BRL"].code == "USD"
    assert data["USD"].codein == "USD"
    assert data["BRL"].codein == "BRL"


@pytest.mark.unit
def test_exchange_negative(monkeypatch):
    user, password = create_test_user()
    currency = "BRL"
    invalid_url = (
        f"https://economia.awesomeapi.com.br/json/wrongg/USD-{currency}"
    )
    with get_session() as session:
        currencies = session.exec(
            select(Person.currency).distinct(Person.currency)
        )
        data = get_rates(currencies=currencies, url=invalid_url)

    assert data["BRL"].name == "api/error"
    assert data["BRL"].value == 0
