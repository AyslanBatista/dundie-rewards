import argparse

from dundie.core import load  # noqa


# Função principal referente ao CLI
def main():
    parser = argparse.ArgumentParser(
        description="Dunder Mifflin rewards CLI",
        # Uma mensagem que será enviada no terminal para o usuario
        epilog="Enjoy and use with cautious",
    )
    # Adicionando primeiro comando
    parser.add_argument(
        "subcommand",
        type=str,  # Tipo de dado que ira receber no subcomando
        help="The subcommand to run",
        choices=("load", "show", "send"),  # comandos
        default="help",
    )
    # Adicionando segundo comando
    parser.add_argument(
        "filepath", type=str, help="File path to load", default=None
    )
    args = parser.parse_args()

    # linha globals()[args.subcommand](args.filepath) se tornará
    # load('arquivo.txt'), assumindo que exista uma função chamada load
    print(*globals()[args.subcommand](args.filepath))
