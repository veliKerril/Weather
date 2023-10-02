class BaseConfig:
    SECRET_KEY = 'fdgfh78@#5?>gfhlsadkjfslkdf>asdlfkjxcvf89dx,v06k'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Weather.db'


class DevelopementConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False

