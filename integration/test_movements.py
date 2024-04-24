import pytest
from click.testing import CliRunner
from conftest import create_test_database

from dundie.cli import movements

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
@create_test_database
def test_movements_positive_call():
    out = cmd.invoke(movements)
    assert "Dunder Mifflin Movements" in out.output
    assert "500" in out.output
    assert "Date" in out.output
    assert "system" in out.output
