#-*- coding: UTF-8 -*-


import io
import pycurl
import logging
from logging.handlers import RotatingFileHandler


class MyFilter1(logging.Filter):
    def __init__(self, levelname):
        self.levelno = {
            'NOTSE': 0,
            'DEBUG': 10,
            'INFO': 20,
            'WARNING': 30,
            'ERROR': 40,
            'CRITICAL': 50,
        }[levelname]

    def filter(self, record):
        if record.levelno < self.levelno and not record.exc_info:
            return True
        else:
            return False


class MyFilter2(logging.Filter):
    def filter(self, record):
        #if record.levelname == 'ERROR' only record exception
        if record.exc_info or record.levelname == 'CRITICAL':
            return True
        else:
            return False


format = logging.Formatter("%(levelname)s-%(asctime)s-%(module)s: %(message)s")


normal_hand = RotatingFileHandler('log/normal.log', maxBytes=2 * 1024 * 1024, backupCount=5)
normal_hand.setLevel(logging.DEBUG)
my_filter = MyFilter1('CRITICAL')
normal_hand.addFilter(my_filter)
normal_hand.setFormatter(format)


crit_hand = logging.FileHandler('log/crit.log')
crit_hand.setLevel(logging.ERROR)
my_filter2 = MyFilter2()
crit_hand.addFilter(my_filter2)
crit_hand.setFormatter(format)


task_log = logging.getLogger('task')
task_log.setLevel(logging.DEBUG)
task_log.addHandler(normal_hand)
task_log.addHandler(crit_hand)