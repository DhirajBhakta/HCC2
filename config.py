import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '123456789987654321'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'nitkhcc@gmail.com'
    MAIL_PASSWORD = 'nitkhccnitkhcc'

    HCC_MAIL_SUBJECT_PREFIX = '[NITK-Health Care Center]'
    HCC_MAIL_SENDER = 'nitkhcc@gmail.com'
    HCC_ADMIN = "fill this shit later"

    MYSQL_DATABASE_USER = 'mysql'
    MYSQL_DATABASE_PASSWORD = 'mysql'
    MYSQL_DATABASE_DB = 'HCCdb'
    MYSQL_DATABASE_HOST = 'localhost'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
