"""
Configuration file for the application.
"""


class Config(object):
    """
    Common configurations
    """
    DEBUG = False


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False


class StagingConfig(Config):
    """
    Staging configurations
    """
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite://" # I use memory db cause "it's just example"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
