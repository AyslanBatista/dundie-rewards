import pytest
from click.testing import CliRunner
from conftest import create_test_database

from dundie.cli import load, main

from .constants import PEOPLE_FILE

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_remove_positive_call_add_command_filter_dept():
    """test command load"""
    cmd.invoke(load, PEOPLE_FILE)
    out = cmd.invoke(main, ["remove", "200", "--dept=Sales"])
    assert "Dunder Mifflin Report" in out.output
    assert "Sales" in out.output
    assert "Direct" not in out.output


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_remove_negative_call_add_command_filter_dept():
    """test command load"""
    cmd.invoke(load, PEOPLE_FILE)
    out = cmd.invoke(main, ["remove", "sdasd", "--dept=Sales"])
    assert "'sdasd' is not a valid integer" in out.output
    assert 2 == out.exit_code


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_remove_positive_call_add_command_filter_email():
    """test command load"""
    cmd.invoke(load, PEOPLE_FILE)
    out = cmd.invoke(main, ["remove", "200", "--email=jim@dundlermifflin.com"])
    assert "Dunder Mifflin Report" in out.output
    assert "jim@du" in out.output
    assert "Dwight" not in out.output


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_remove_negative_call_add_command_filter_email():
    """test command load"""
    cmd.invoke(load, PEOPLE_FILE)
    out = cmd.invoke(
        main, ["remove", "-200", "--email=jim@dundlermifflin.com"]
    )
    assert "No such option:" in out.output
    assert "-2" in out.output
    assert 2 == out.exit_code
