import os
import sys
from functools import wraps

import rich_click as click
from rich.console import Console
from rich.theme import Theme
from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person, User

NUMBER_ATTEMPTS: int = 3
FIRST_CHECK = False

custom_theme = Theme(
    {"info": "bold cyan", "warning": "magenta", "danger": "bold red"}
)
console = Console(theme=custom_theme)


class AuthenticationLimitError(Exception):
    """
    Exceção personalizada para erros de autenticação.
    """


def access_allowed() -> bool:
    """Checking if the username and password
    passed match the credentials saved in the database
    """
    email = os.getenv("DUNDIE_EMAIL")
    senha = os.getenv("DUNDIE_PASSWORD")
    with get_session() as session:
        filter_user = session.exec(
            select(Person)
            .join(User)
            .where(Person.email == email)
            .where(User.password == senha)
        ).first()
        if filter_user is None:
            return False

    return True


def request_login():
    """Requests username and password and exports as environment variables"""
    console.print(
        "Please enter the email and then the password.\n", style="info"
    )
    email = console.input(
        "👤 [bold green]Email:[/] ",
    )
    password = console.input("🔒 [bold green]Password[/]: ", password=True)

    os.environ["DUNDIE_EMAIL"] = email
    os.environ["DUNDIE_PASSWORD"] = password


def login_attempts(attempts: int) -> int:
    """Measure the attempts, and call the `request_login` function

    Args:
        attempts (int): current attempts

    Returns:
        int: returns -1 which will be removed from remaining attempts
    """
    if attempts == NUMBER_ATTEMPTS:
        console.print(
            "\n ⚠  [WARNING] You need to be logged in "
            "to access this function.\n",
            style="warning",
        )
    else:
        console.print(
            f"\n❌ [ERROR] email or password is incorrect,"
            f" {attempts} attempts left.\n",
            style="danger",
        )
    request_login()
    return -1


def check_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global FIRST_CHECK
        attempts = NUMBER_ATTEMPTS
        try:
            while attempts > 0:
                if access_allowed():
                    # Se for primeira chamada da função ele retorna a aprovação
                    if not FIRST_CHECK:
                        email = os.getenv("DUNDIE_EMAIL")
                        console.print(
                            f"\n✅ [bold][AUTHORIZED][/] You are logged into"
                            f" the account [blue]{email!r}[/].\n",
                            style="green",
                        )
                        FIRST_CHECK = True

                    # Se o usuário estiver logado a função original é executada
                    return func(*args, **kwargs)

                else:
                    attempts += login_attempts(attempts)
                    continue
            raise AuthenticationLimitError(
                "\n❌ [ERROR] You have reached the authentication limit,"
                " please try again later...",
            )
        except AuthenticationLimitError as e:
            click.echo(click.style(e, bold=True, fg="white", bg="red"))
            sys.exit(1)

    return wrapper
