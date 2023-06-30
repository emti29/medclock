class Config:
    DEBUG = True
    TESTING = True

    #Configurar base de datos

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:qwerty@localhost:3306/medclock_db"


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    SECRET_KEY = 'dev'
    DEBUG = False
    TESTING = True