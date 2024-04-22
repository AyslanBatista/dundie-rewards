import pkg_resources
import rich_click as click
from rich.table import Table

from dundie import core
from dundie.settings import console

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
    headers = ["name", "email", "dept", "role", "currency", "created"]
    for header in headers:
        table.add_column(header, style="green")

    result = core.load(filepath)
    for person in result:
        table.add_row(*[str(value) for value in person.values()])

    # Console vai calcular o tamanho do terminal para exibição da tabela
    console.print(table)


@main.command()
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.option("--output", default=None)
def show(output, **query):
    """Show information about users"""
    result = core.read(show=True, **query)
    if output:
        core.generating_json_file(data=result, path=output)

    table = Table(
        title="Dunder Mifflin Report", style="cyan", title_style="bold"
    )
    for key in result[0]:
        table.add_column(key.title().replace("_", " "), style="green")

    for person in result:
        person["value"] = f"{person['value']:.2f}"
        person["balance"] = f"{person['balance']:.2f}"
        table.add_row(*[str(value) for value in person.values()])
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
    """Remove points to the user or dept"""

    core.add(-value, **query)
    ctx.invoke(show, **query)


@main.command()
@click.argument("value", type=click.INT, required=True)
@click.option("--dept", required=False)
@click.option("--email", required=False)
def transfer(value, **to):
    """Transfer points from one user to another user or department"""
    new_value, data_sender = core.transfer(value, **to)
    if to["email"]:
        console.print(
            f"\n💸 Success.. [bold green]{new_value}[/] points transferred "
            f"from your account to account by {data_sender[0]['email']!r}."
        )

    if to["dept"]:
        console.print(
            f"\n💸 Success.. [bold green]{new_value}[/] points transferred "
            f"from your account to the account of [bold]{len(data_sender)}[/] "
            f"{data_sender[0]['dept']!r} department employees."
        )


@main.command()
def movements():
    """Displays the movement history of the logged in user"""
    table = Table(
        title="Dunder Mifflin Movements", style="cyan", title_style="bold"
    )
    movements = core.movements()

    for key in movements[0]:
        table.add_column(key.title().replace("_", " "), style="green")

    for movement in movements:
        table.add_row(*[str(value) for value in movement.values()])

    console.print(table)
