from datetime import datetime

import pytest
from click.testing import CliRunner
from conftest import create_test_database

from dundie.cli import load, show

from .constants import PEOPLE_FILE

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_show_positive_call_show_command_table_structure():
    """test command load"""
    cmd.invoke(load, PEOPLE_FILE)
    out = cmd.invoke(show)
    # Manter 6 caracteres, por causa da responsividade do terminal
    expected_strings = [
        "Dunder Mifflin Report",
        "Name",
        "Email",
        "Dept",
        "Role",
        "Balance",
        "Last",
        "Moveme",
        "Curren",
        "Value",
    ]
    for expected_string in expected_strings:
        assert expected_string in out.output


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_show_positive_call_show_command_table_content():
    """test command load"""
    cmd.invoke(load, PEOPLE_FILE)
    out = cmd.invoke(show)
    day_now = datetime.today().strftime("%d/%m/")
    # Manter 6 caracteres, por causa da responsividade do terminal
    expected_strings = [
        "Jim",
        "Halper",
        "Dwight",
        "Lewis",
        "Sales",
        "chrute",
        "Manage",
        "USD",
        "Direct",
        day_now,
        "500.00",
        "100.00",
    ]
    for expected_string in expected_strings:
        assert expected_string in out.output


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_show_positive_call_show_command_with_dept_params():
    """test command load"""
    cmd.invoke(load, PEOPLE_FILE)
    out = cmd.invoke(show, "--dept=Sales")
    expected_strings = [
        "Jim",
        "Halper",
        "Dwight",
        "Schru",
        "Sales",
        "Salesm",
        "Manage",
    ]
    for expected_string in expected_strings:
        assert expected_string in out.output

    no_expected_strings = [
        "Gabe",
        "Lewis",
        "Direct",
        "glewis",
    ]
    for no_expected_string in no_expected_strings:
        assert no_expected_string not in out.output


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_show_positive_call_show_command_with_email_params():
    """test command load"""
    cmd.invoke(load, PEOPLE_FILE)
    out = cmd.invoke(show, "--email=schrute@dundlermifflin.com")
    expected_strings = [
        "Dwight",
        "Schrut",
        "Sales",
        "Manage",
        "schrut",
    ]
    for expected_string in expected_strings:
        assert expected_string in out.output

    no_expected_strings = [
        "Gabe",
        "Lewis",
        "Direct",
        "glewis",
    ]
    for no_expected_string in no_expected_strings:
        assert no_expected_string not in out.output


# @pytest.mark.integration
# @pytest.mark.medium
# @create_test_database
# def test_show_positive_call_show_command_with_output_params():
#     """test command load"""
#     cmd.invoke(load, PEOPLE_FILE)
#     out = cmd.invoke(
#         show,
#         "--dept=Sales",
#     )
