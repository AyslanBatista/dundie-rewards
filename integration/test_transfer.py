import pytest
from click.testing import CliRunner
from conftest import create_test_database

from dundie.cli import load, main

from .constants import PEOPLE_FILE

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_transfer_positive_call_show_command_filter_dept():
    cmd.invoke(load, PEOPLE_FILE)
    out = cmd.invoke(main, ["transfer", "200", "--dept=Sales"])

    assert "400" in out.output
    assert "Sales" in out.output


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_transfer_negative_call_show_command_filter_dept():
    cmd.invoke(load, PEOPLE_FILE)
    out = cmd.invoke(main, ["transfer", "dsaddas", "--dept=Sales"])

    assert "'dsaddas' is not a valid integer" in out.output
    assert 2 == out.exit_code


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_transfer_positive_call_show_command_filter_email():
    cmd.invoke(load, PEOPLE_FILE)
    out = cmd.invoke(
        main, ["transfer", "200", "--email=jim@dundlermifflin.com"]
    )

    assert "200" in out.output
    assert "jim@du" in out.output


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_transfer_negative_call_show_command_filter_email():
    cmd.invoke(load, PEOPLE_FILE)
    out = cmd.invoke(
        main, ["transfer", "-200", "--email=jim@dundlermifflin.com"]
    )

    assert "No such option:" in out.output
    assert "-2" in out.output
    assert 2 == out.exit_code
