import os

import pytest
from conftest import create_test_user

from dundie.core import load

from .constants import PEOPLE_FILE


@pytest.fixture(scope="function", autouse=True)
def export_variables_for_test(request):
    """Exporta as variáveis de ambiente para os testes"""
    user, password = create_test_user()
    os.environ["DUNDIE_USER"] = user
    os.environ["DUNDIE_PASSWORD"] = password
    yield
    del os.environ["DUNDIE_USER"]
    del os.environ["DUNDIE_PASSWORD"]


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_has_2_people(request):
    """Test function load function."""
    assert len(load(PEOPLE_FILE)) == 3


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_first_name_starts_with_j(request):
    """Test function load function."""
    assert load(PEOPLE_FILE)[0]["name"] == "Jim Halpert"


@pytest.mark.unit
@pytest.mark.high
def test_negative_filenotfound(request):
    """Test function load function."""
    with pytest.raises(FileNotFoundError):
        load("assets/invalid.csv")
