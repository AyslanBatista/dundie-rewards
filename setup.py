import os

from setuptools import find_packages, setup


# Função muito util para ter nos projetos para ler diferentes arquivos
def read(*paths):
    """Read the contests of a text file safely.
    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """
    # Pegando o caminho de onde está o arquivo atual
    rootpah = os.path.dirname(__file__)
    filepath = os.path.join(rootpah, *paths)
    with open(filepath) as file_:
        return file_.read().strip()


# Usa a função "read" para ler um arquivo e obter o conteudo
def read_requirements(path):
    """Return a list of requirements from a text file"""
    return [
        line.strip()
        for line in read(path).split("\n")
        # ignora linhas que começa com
        if not line.startswith(("#", "git+", '"', "-"))
    ]


setup(
    # Nome do Programa | pip install dundie
    name="dundie",
    # x.y.z | Major.Minor.Patch
    # X=Algo muito significativo
    # y=Novas funcionalidades
    # z=Resolver bug ou pequenas mudanças
    version="0.1.1",
    description="Reward Point System for Dunder Mifflin",
    # Será adicionar o README na decrição do programa no PYPI
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Ayslan Batista",
    python_requires=">=3.8",  # Meu programa só roda em versão maior que 3.8
    # packages=["dundie"] Durante o build os pacotes serão apenas
    # os programas que estão escritos dentro da pasta "dundie"
    # pode ser usado o find_packages()
    # Ele ira procurar todas as pastas que contem __init__.py
    packages=find_packages(exclude=["integration"]),
    include_package_data=True,  # vai verificar o arquivo MANIFEST.in no build
    # Lista de quais são os nomes dos entrypoints e os pacotes entrypoints
    entry_points={
        # Forma de usar diretamente o programa ex: dundie --version
        "console_scripts": ["dundie = dundie.__main__:main"]
    },
    # Nome dos pacotes que o nosso projeto precisa
    install_requires=read_requirements("requirements.txt"),
    # Dependencias Extras Opcionais | pip install -e '.[dev]'
    extras_require={
        "test": read_requirements("requirements.test.txt"),
        "dev": read_requirements("requirements.dev.txt"),
    },
)
