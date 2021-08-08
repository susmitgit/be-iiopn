import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


class ApiConfig:
    DEFAULT_PAGE_SIZE = 2
    DEFAULT_API_RATE_LIMIT = ["20000/day", "3000/hour", "500/minute"]

    @staticmethod
    def init_log(config_name='production'):
        log_level = logging.DEBUG
        if config_name == 'production':
            log_level = logging.ERROR

        logging.basicConfig(filename='logs/be_server.log', level=log_level,
                            format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    @staticmethod
    def init_rate_limit(app_instance=None):
        return Limiter(
            app_instance,
            key_func=get_remote_address,
            default_limits=ApiConfig.DEFAULT_API_RATE_LIMIT
        )
