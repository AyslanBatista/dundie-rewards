import os

SMTP_HOST = "locahost"
SMTP_PORT = 8025
SMTP_TIMEOUT = 5

EMAIL_FROM = "master@dundie.com"

ROOTH_PATH = os.path.dirname(__file__)
DATABASE_PATH = os.path.join(ROOTH_PATH, "..", "assets", "database.json")
