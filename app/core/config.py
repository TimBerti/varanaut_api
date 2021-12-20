from pydantic import BaseSettings
from dotenv import load_dotenv
import os


try:
    load_dotenv()
except:
    debug = False
else:
    debug = True


class Settings(BaseSettings):
    DEBUG = debug

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 3600

    SECRET_KEY = os.environ['SECRET_KEY']
    SECURITY_ALGORITHM = os.environ['SECURITY_ALGORITHM']


settings = Settings()
