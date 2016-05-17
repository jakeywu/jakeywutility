# __author__ = 'jakey'

import logging
import logging.config
import os

from utility.config.logging_conf import logging_conf_dict


def get_logger(path="", name="root"):
    """
    通用日志
    :param path: 日志路径, 默认为空
    :param name: root 和　console
    :return:
    """
    if path and not os.path.isdir(path):
        raise TypeError("非法日志文件路径...")

    log_path = os.path.join(path, "py_log/")
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    logging.config.dictConfig(logging_conf_dict(log_path))
    return logging.getLogger(name)
