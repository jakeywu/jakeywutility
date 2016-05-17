# __author__ = 'jakey'

import time
import functools


def timeit(function):
    """
    装饰器 计算函数执行时间 单位:ms
    :param function:
    :return:
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        begin = time.clock()
        exec_time = function(*args, **kwargs)
        print('function %s() execute time is: %s ms' % (function.__name__, (time.clock()-begin)*1000))
        return exec_time
    return wrapper
