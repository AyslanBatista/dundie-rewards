import logging
import os
from logging import handlers

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
log = logging.getLogger("dundie")  # Criando stancia de log
# Objeto de formatação de como será exibido os logs
fmt = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s "
    "l:%(lineno)d f:%(filename)s: %(message)s"
)


# Controle de logs do usuario pela variavel de ambiente
# export LOG_LEVEL=debug
# export serve para ativar o log level em formato DEV, para exibir os debug
def get_logger(logfile="dundie.log"):
    """Returns a configured logger."""

    # Responsavel por salvar os log em arquivo
    fh = handlers.RotatingFileHandler(
        # Nome do arquivo
        logfile,
        # maxBytes = 10**6 Tamanho maximo do arquivo, depois cria outro arquivo
        maxBytes=10**6,
        # backupCount=10 >> Quantidade de arquivos para manter no backup
        backupCount=10,
    )

    fh.setLevel(LOG_LEVEL)  # Nivel que será exibido

    fh.setFormatter(fmt)  # Adicionando a formtação ao Handler que foi criado
    log.addHandler(fh)  # Por fim adiciona o Handler ao log
    return log
