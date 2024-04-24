import os
from decimal import Decimal

import pytest
from conftest import create_test_database

from dundie.core import generating_json_file, load, read

from .constants import PEOPLE_FILE


@pytest.mark.unit
@create_test_database
def test_generating_json_file_positive():
    load(PEOPLE_FILE)
    current_directory = os.getcwd()
    path = os.path.join(current_directory, "foo.txt")
    data = read()
    generating_json_file(data=data, path=path)
    with open(path) as file_:
        content = file_.read()

    for data_user in data:
        for key, value in data_user.items():
            if isinstance(value, Decimal):
                value = str(value)
            assert key in content
            assert value in content


@pytest.mark.unit
@create_test_database
def test_generating_json_file_negative():
    load(PEOPLE_FILE)
    path = os.path.join("/root/", "foo.txt")
    data = read()
    with pytest.raises(SystemExit) as e:
        generating_json_file(data=data, path=path)

    assert e.type == SystemExit
    assert e.value.code == 4
