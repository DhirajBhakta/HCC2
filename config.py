import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '123456789987654321'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'dhirajbhakta110@gmail.com'
    MAIL_PASSWORD = 'silverhorse'
    FLASKY_MAIL_SUBJECT_PREFIX = '[_H_C_C_]'
    FLASKY_MAIL_SENDER = 'Dhiraj Bhakta <dhirajbhakta110@gmail.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = 'student'
    MYSQL_DATABASE_DB = 'HCCdb'
    MYSQL_DATABASE_HOST = 'localhost'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI =  'mysql+pymysql://root:student@localhost/HCCdb'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}