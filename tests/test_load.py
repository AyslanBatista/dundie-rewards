import os
import uuid

import pytest

from dundie.core import load

from .constants import PEOPLE_FILE


def setup_module():
    print()
    print("roda antes dos testes desse modulo\n")


def teardown_module():
    print()
    print("roda apos os testes desse modulo\n")


@pytest.fixture(scope="function", autouse=True)
def create_new_file(tmpdir):
    file_ = tmpdir.join("new_file.txt")
    file_.write("isso é sujeira...")
    yield  # Função do test ira rodar nesse momento
    file_.remove()  # Remove o arquivo que foi criado


@pytest.mark.unit
@pytest.mark.high
def test_load(request):
    """Test load function."""

    filepath = f"arquivo_indesejado-{uuid.uuid4()}.txt"
    # ele irá rodar esse comando para apagar o arquivo
    # que foi criado depois de rodar os test da função
    request.addfinalizer(lambda: os.unlink(filepath))

    with open(filepath, "w") as file_:
        file_.write("dados uteis somente para o test")

    assert len(load(PEOPLE_FILE)) == 2
    assert load(PEOPLE_FILE)[0][0] == "J"


@pytest.mark.unit
@pytest.mark.high
def test_load2():
    """Test function load function."""

    with open(f"arquivo_indesejado-{uuid.uuid4()}.txt", "w") as file_:
        file_.write("dados uteis somente para o teste")

    assert len(load(PEOPLE_FILE)) == 2
    assert load(PEOPLE_FILE)[0][0] == 'J'
