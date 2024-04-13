import json

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

    This cli application controls Dunder Mifflin rewards.

    - admins can load information tot he people database and assign points.
    - users can view reports and transfer points.

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
    headers = ["email", "name", "dept", "role", "created"]
    for header in headers:
        table.add_column(header, style="green")

    result = core.load(filepath)
    for person in result:
        table.add_row(*[str(value) for value in person.values()])

    # Console vai calcular o tamanho do terminal para exibição da tabela
    console = Console()
    console.print(table)


@main.command()
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.option("--output", default=None)
def show(output, **query):
    """Show information about users"""
    result = core.read(**query)
    if output:
        with open(output, "w") as output_file:
            output_file.write(json.dumps(result))

    if not result:
        print("Nothing to show")

    table = Table(
        title="Dunder Mifflin Report", style="cyan", title_style="bold"
    )
    for key in result[0]:
        table.add_column(key.title().replace("_", " "), style="green")

    for person in result:
        table.add_row(*[str(value) for value in person.values()])

    console = Console()
    console.print(table)


@main.command()
@click.argument("value", type=click.INT, required=True)
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.pass_context  # Exibir o "show" depois de rodar a função
def add(ctx, value, **query):
    """Add points to the user or dept"""
    core.add(value, **query)

    ctx.invoke(show, **query)


@main.command()
@click.argument("value", type=click.INT, required=True)
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.pass_context  # Exibir o "show" depois de rodar a função
def remove(ctx, value, **query):
    """Add points to the user or dept"""

    core.add(-value, **query)
    ctx.invoke(show, **query)
