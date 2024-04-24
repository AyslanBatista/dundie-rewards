import os
import sys
from functools import wraps

import rich_click as click
from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person, User
from dundie.settings import console
from dundie.utils.log import log

NUMBER_ATTEMPTS: int = 3
FIRST_CHECK = False


class AuthenticationLimitError(Exception):
    pass


def access_allowed() -> bool:
    """Checking if the username and password
    passed match the credentials saved in the database
    """
    email = os.getenv("DUNDIE_EMAIL")
    senha = os.getenv("DUNDIE_PASSWORD")

    if (email and senha) is None:
        return None

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
        message_login_required = (
            "\n ⚠  [WARNING] You need to be logged in "
            "to access this function.\n"
        )
        console.print(message_login_required, style="warning")
        log.warning(message_login_required.strip())

    else:
        message_attempt_error = (
            f"\n❌ [ERROR] email or password is incorrect,"
            f" {attempts} attempts left.\n"
        )
        console.print(message_attempt_error, style="danger")
        log.error(message_attempt_error.strip())
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
                    # Se for primeira chamada da função
                    # ele retorna a aprovação do login
                    if not FIRST_CHECK:
                        email = os.getenv("DUNDIE_EMAIL")
                        message_sucesss_login = (
                            f"\n✅ [bold][AUTHORIZED][/] You are logged into"
                            f" the account [blue]{email!r}[/].\n"
                        )

                        console.print(message_sucesss_login, style="green")
                        log.info(message_sucesss_login.strip())
                        FIRST_CHECK = True

                    # Se o usuário estiver logado a função original é executada
                    return func(*args, **kwargs)

                if access_allowed() is None:
                    attempts += login_attempts(attempts)
                    continue

                if not access_allowed():
                    message_attempt_error = (
                        "\n❌ [ERROR] email or password exported in"
                        "environment variables are incorrect\n"
                    )
                    console.print(message_attempt_error, style="danger")
                    log.error(message_attempt_error.strip())
                    attempts += login_attempts(attempts)
                    continue

            raise AuthenticationLimitError(
                "\n❌ [ERROR] You have reached the authentication limit,"
                " please try again later..."
            )
        except AuthenticationLimitError as e:
            log.error(str(e).strip())
            click.echo(click.style(e, bold=True, fg="white", bg="red"))
            sys.exit(5)

    return wrapper
