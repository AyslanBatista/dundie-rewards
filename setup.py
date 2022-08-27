# setuptools | pyproject | external build tools (potry, flit)
# Transformar um programa em instalável | pip install -e . | python setup.py build

from setuptools import find_packages, setup

setup(
    name="dundie",
    version="0.1.0",  # x.y.z.
    description="Reward Point System for Dunder Mifflin",
    author="Ayslan Batista",
    packages=find_packages(),  # todas as pasta que contem __init__
    entry_points={ # Criando uma chamada de execução via terminal pelo nome do programa 
        "console_scripts": [
            "dundie = dundie.__main__:main"
        ]
    }, 
)
