class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'us-cdbr-east-06.cleardb.net'
    MYSQL_USER = 'bbd292aa23aeaf'
    MYSQL_PASSWORD = 'ece55924'
    MYSQL_DB = 'heroku_978ea61906c2949'


config = {
    'development': DevelopmentConfig
}
