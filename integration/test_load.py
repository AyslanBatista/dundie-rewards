import os

import pytest
from click.testing import CliRunner
from conftest import create_test_user

from dundie.cli import load, main

from .constants import PEOPLE_FILE

cmd = CliRunner()


@pytest.fixture(scope="function", autouse=True)
def export_variables_for_test(request):
    """Exporta as variáveis de ambiente para os testes"""
    user, password = create_test_user()
    os.environ["DUNDIE_USER"] = user
    os.environ["DUNDIE_PASSWORD"] = password
    yield
    del os.environ["DUNDIE_USER"]
    del os.environ["DUNDIE_PASSWORD"]


@pytest.mark.integration
@pytest.mark.medium
def test_load_positive_call_load_command():
    """test command load"""
    out = cmd.invoke(load, PEOPLE_FILE)
    assert "Dunder Mifflin Associates" in out.output


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize("wrong_command", ["loady", "carrega", "start"])
def test_load_negative_call_load_command_with_wrong_params(wrong_command):
    """test command load"""
    out = cmd.invoke(main, wrong_command, PEOPLE_FILE)
    assert out.exit_code != 0
    assert f"No such command '{wrong_command}'." in out.output
