"""Core=Funções principais do programa"""

from dundie.utils.log import get_logger

log = get_logger


def load(filepath):
    """Carrega dados do caminho do arquivo para o banco de dados

    Args:
        filepath (_type_): _description_
    """
    try:
        with open(filepath) as file_:
            return [line.strip() for line in file_.readlines()]
    except FileNotFoundError as e:
        log.error(str(e))
        raise e
