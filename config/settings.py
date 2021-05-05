from datetime import timedelta

DEBUG = True
SERVER_NAME = 'localhost:8000'

# SQLAlchemy.
db_uri = 'sqlite:///database/payroll.db'
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
