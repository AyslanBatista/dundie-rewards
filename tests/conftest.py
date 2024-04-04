import pytest

MARKER = """\
integration: Mark integration tests
unit: Mark unit tests
high: High Priority
medium: Medium Priority
low: low Priority
"""


def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line('markers', line)


# Dados fixos - dados que temos para popular durante o test
# autouse=True - Automaticamente todos os test do projeto irão usar a fixture
@pytest.fixture(autouse=True)
def go_to_tmpdir(request):  # mandar toda a "sujeira" para o tmp
    # Quem fornece o request é o pytest | injeção de dependencias
    tmpdir = request.getfixturevalue("tmpdir")  # Diretorio temporario
    # With abaixo Muda o diretorio atual
    # Ele ira rodar cada test dentro do contexto abaixo
    with tmpdir.as_cwd():
        yield  # protocolo de generators | para que cada função rode aqui
