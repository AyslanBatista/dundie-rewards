import pytest
from conftest import create_test_database

from dundie.core import load

from .constants import PEOPLE_FILE


@pytest.mark.unit
@pytest.mark.high
@create_test_database
def test_load_positive_has_2_people():
    """Test function load function."""
    assert len(load(PEOPLE_FILE)) == 3


@pytest.mark.unit
@pytest.mark.high
@create_test_database
def test_load_positive_first_name_starts_with_j():
    """Test function load function."""
    assert load(PEOPLE_FILE)[0]["name"] == "Jim Halpert"


@pytest.mark.unit
@pytest.mark.high
@create_test_database
def test_negative_filenotfound():
    """Test function load function."""
    with pytest.raises(SystemExit) as e:
        load("assets/invalid.csv")

    assert e.type == SystemExit
    assert e.value.code == 1
