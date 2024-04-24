import os

import pytest
from conftest import create_test_database, create_test_user

from dundie.core import load
from dundie.utils.login import access_allowed, check_login, login_attempts

from .constants import PEOPLE_FILE


@pytest.mark.unit
@create_test_database
def test_check_login_allowed():
    @check_login
    def my_function():
        return "Original function performed"

    result = my_function()
    assert result == "Original function performed"


@pytest.mark.unit
def test_login_positive_no_export_variables_(monkeypatch):
    user, password = create_test_user()
    inputs = iter([user, password])
    monkeypatch.setattr(
        "dundie.utils.login.console.input", lambda _, **kwargs: next(inputs)
    )

    @check_login
    def my_function():
        return "Original function performed"

    resultado = my_function()

    assert os.environ["DUNDIE_EMAIL"] == user
    assert os.environ["DUNDIE_PASSWORD"] == password
    assert resultado == "Original function performed"


@pytest.mark.unit
def test_login_negative_authentication_limit_error(monkeypatch):
    create_test_user()
    user = "wrong@test.com"
    password = "wrongpassword"
    inputs = iter([user, password] * 3)
    monkeypatch.setattr(
        "dundie.utils.login.console.input", lambda _, **kwargs: next(inputs)
    )
    with pytest.raises(SystemExit) as e:

        @check_login
        def my_function():
            return "Original function performed"

        my_function()

    assert e.type == SystemExit
    assert e.value.code == 5


@pytest.mark.unit
@create_test_database
def test_login_positive_export_variables():
    assert access_allowed() is True


@pytest.mark.unit
@create_test_database
def test_login_positive_export_variables_wrong():
    load(PEOPLE_FILE)
    os.environ["DUNDIE_EMAIL"] = "jim@dundlermifflin.com"
    os.environ["DUNDIE_PASSWORD"] = "wrongpassword"
    assert access_allowed() is False


@pytest.mark.unit
def test_login_attempts_warning(monkeypatch, capsys):
    user = "wrong@test.com"
    password = "wrongpassword"
    inputs = iter([user, password])
    monkeypatch.setattr(
        "dundie.utils.login.console.input",
        lambda _, **kwargs: next(inputs),
    )

    result = login_attempts(3)
    captured = capsys.readouterr()

    assert "WARNING" in captured.out
    assert result == -1


@pytest.mark.unit
def test_login_attempts_error(monkeypatch, capsys):
    user = "wrong@test.com"
    password = "wrongpassword"
    inputs = iter([user, password])
    monkeypatch.setattr(
        "dundie.utils.login.console.input",
        lambda _, **kwargs: next(inputs),
    )

    result = login_attempts(2)
    captured = capsys.readouterr()

    assert "ERROR" in captured.out
    assert "2" in captured.out
    assert result == -1
