import os

TEST_PATH: str = os.path.dirname(__file__)
PEOPLE_FILE: str = os.path.join(TEST_PATH, "assets/people.csv")
USER_TEST: dict = {
    "currency": "BRL",
    "role": "CEO",
    "dept": "C-Level",
    "name": "Test",
    "email": "test@dundlermifflin.com",
}
