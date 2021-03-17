# -*- encoding: utf-8 -*-
import os

class ProdConfig():
    # Production configuration
    env = 'prod'
    debug = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'postgresql://localhost/example')

class DevConfig():
    # Development configuration
    # env = 'dev'
    debug = True
    DB_NAME = 'ews'
    