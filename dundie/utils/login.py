import os
from functools import wraps
from getpass import getpass

from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person, User

NUMBER_ATTEMPTS: int = 3

first_check = False


class AuthenticationLimitError(Exception):
    """
    Exceção personalizada para erros de autenticação.
    """

    def __init__(self, message):
        self.message = message


def access_allowed() -> bool:
    """Checking if the username and password
    passed match the credentials saved in the database
    """
    user = os.getenv("DUNDIE_USER")
    senha = os.getenv("DUNDIE_PASSWORD")
    with get_session() as session:
        filter_user = session.exec(
            select(Person)
            .join(User)
            .where(Person.email == user)
            .where(User.password == senha)
        ).first()
        if filter_user is None:
            return False

    return True


def request_login():
    """Requests username and password and exports as environment variables"""
    print("Please enter the email and then the password")
    user = input("User: ")
    password = getpass("Password: ", stream=None)

    os.environ["DUNDIE_USER"] = user
    os.environ["DUNDIE_PASSWORD"] = password


def login_attempts(attempts: int) -> int:
    """Measure the attempts, and call the `request_login` function

    Args:
        attempts (int): current attempts

    Returns:
        int: returns -1 which will be removed from remaining attempts
    """
    if attempts == NUMBER_ATTEMPTS:
        print(
            "\n❌ [ERROR] You need to be logged in "
            "to access this function.\n"
        )
    else:
        print(
            f"\n❌ [ERROR] Username or password is incorrect,"
            f" {attempts} attempts left\n"
        )
    request_login()
    return -1


def check_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global first_check
        attempts = NUMBER_ATTEMPTS
        while attempts > 0:
            if access_allowed():
                # Se for a primeira chamada da função ele retorna a aprovação
                if not first_check:
                    user = os.getenv("DUNDIE_USER")
                    print(
                        f"\n✅ [AUTHORIZED] You are logged into"
                        f" the account {user!r}\n"
                    )
                    first_check = True

                # Se o usuário estiver logado, a função original é executada
                return func(*args, **kwargs)

            else:
                attempts += login_attempts(attempts)
                continue
        raise AuthenticationLimitError(
            "❌ [ERROR] You have reached the authentication limit,"
            " please try again later"
        )

    return wrapper
