# test

class BaseConfig(object):
    MONGODB_SETTINGS = {

    }
    SECRET_KEY = "MY_APP_SECURE"
    DEBUG = True


class TestingConfig(object):
    """Development configuration."""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
