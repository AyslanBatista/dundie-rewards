import pkg_resources
import rich_click as click
from rich.console import Console
from rich.table import Table

from dundie import core

# Conjunto de configurações do Rich
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True


@click.group()  # Responsavel pelos subcomandos
@click.version_option(  # pegando a versão do programa, dundie --version
    pkg_resources.get_distribution("dundie").version
)
def main():
    """Dunder Mifflin Rewards System.

    This cli application controls DM rewards.
    """


# Qualquer nome de função se tonar um subcomando para o cli
@main.command()
@click.argument("filepath", type=click.Path(exists=True))  # checkar argumento
def load(filepath):  # injeção de dependencia
    """Loads the file to the database

        ## Features

    - Validdates data
    - Parses the file
    - Load to database
    """
    table = Table(
        title="Dunder Mifflin Associates", style="cyan", title_style="bold"
    )
    headers = ["name", "dept", "role", "created", "e-mail"]
    for header in headers:
        table.add_column(header, style="green")

    result = core.load(filepath)
    for person in result:
        table.add_row(*[str(value) for value in person.values()])

    # Console vai calcular o tamanho do terminal para exibição da tabela
    console = Console()
    console.print(table)
