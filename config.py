import os

# set DATABASE_URL=postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/food_shop


class Config:
    DEBUG = True
    SECRET_KEY = "secret_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
