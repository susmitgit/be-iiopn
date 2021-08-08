

class Config(object):
    """
    Common configurations
    """

    SECRET_KEY = "MY_APP_SECURE"
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

