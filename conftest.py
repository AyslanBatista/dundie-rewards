import warnings
import os

from dundie.utils.db import add_person
from dundie.database import get_session
import pytest
from tests.constants import USER_TEST

from unittest.mock import patch
from sqlmodel import create_engine, select
from dundie import models


from sqlalchemy.exc import SAWarning


warnings.filterwarnings("ignore", category=SAWarning)


MARKER = """\
unit: Mark unit tests
integration: Mark integration tests
high: High Priority
medium: Medium Priority
low: Low Priority
"""


def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)


# cada teste tem um diretorio no tmp
@pytest.fixture(autouse=True)
def go_to_tmpdir(request):  # injeção de dependencias
    tmpdir = request.getfixturevalue("tmpdir")
    with tmpdir.as_cwd():
        yield  # protocolo de generators


# Criando um banco de dados para cada teste no diretorio do tmp de cada teste
@pytest.fixture(autouse=True, scope="function")
def setup_testing_database(request):
    """For each test, create a database file on tmpdir
    force database.py to use that filepath.
    """
    tmpdir = request.getfixturevalue("tmpdir")
    test_db = str(tmpdir.join("database.test.db"))
    engine = create_engine(f"sqlite:///{test_db}")
    models.SQLModel.metadata.create_all(bind=engine)
    with patch("dundie.database.engine", engine):
        yield


def create_test_user():
    """Creating a test user in the database"""
    with get_session() as session:
        user = USER_TEST["email"]
        add_person(session, models.Person(**USER_TEST))
        session.commit()
        filtro = session.exec(
            select(models.Person, models.User)
            .join(models.User)
            .where(models.Person.email == user)
        ).first()
    return user, filtro[1].password


def create_test_database(func):
    def wrapper(*args, **kwargs):
        email, password = create_test_user()
        os.environ["DUNDIE_EMAIL"] = email
        os.environ["DUNDIE_PASSWORD"] = password
        try:
            return func(*args, **kwargs)
        finally:
            del os.environ["DUNDIE_EMAIL"]
            del os.environ["DUNDIE_PASSWORD"]

    return wrapper
