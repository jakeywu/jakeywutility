# __author__ = 'jakey'

import random

from utility.config.requests_conf import USER_AGENTS


def get_user_agent():
    """
    获取随机代理
    :return:
    """
    return random.choice(USER_AGENTS)
