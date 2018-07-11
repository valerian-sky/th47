#-*- coding: UTF-8 -*-

import sys
import time
import random
import signal
import logging
import threading


reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger('task')


class Task(object):
    def __init__(self, config, gglm):
        self.thread_vector = config.thread_vector
        self.session_num_per_hour = config.session_num_per_hour
        self.gglm = gglm
        self.term_flag = False

    class WorkThread(threading.Thread):
        def __init__(self, task, start_time):
            super(type(self), self).__init__()
            self.setDaemon(True)
            self.start_time = start_time
            self.task = task

        def run(self):
            logger.debug('start: %d, %s start!!!' % (self.start_time, self.getName()))

            _time = random.random() * 100 + 100
            time.sleep(_time)

            self.cpc_count = 0
            for i in range(self.task.session_num_per_hour):
                try:
                    obj = self.task.gglm()
                    obj.start()
                    self.cpc_count += obj.cpc_count
                    _time = random.random() * 160 + 190
                    time.sleep(_time)
                except Exception as e:
                    print e
                    logger.error(str(e) + '  具体栈回溯信息查看crit.log  ')
                    logger.exception(e)

            logger.debug('start_: %d, %s end!!! cpc: %d, ' % (self.start_time, self.getName(), self.cpc_count, ))

        def _weighted_choice_sub(self, weights):
            rnd = random.random() * sum(weights)
            for i, w in enumerate(weights):
                rnd -= w
                if rnd < 0:
                    return i

    #运行工作线程的控制线程
    class ControlThread(threading.Thread):
        def __init__(self, start_time, task, thread_num):
            super(type(self), self).__init__()
            self.setDaemon(True)
            self.start_time = start_time
            self.task = task
            self.thread_num = thread_num
            self.start()
            #设置线程栈大小为4M  3G / 4M 约等于 768  即单进程最多能创建768个线程
            threading.stack_size(4 * 1024 * 1024)

        def run(self):
            thread_list = []
            try:
                for i in range(self.thread_num):
                    thread = self.task.WorkThread(self.task, self.start_time)
                    thread_list.append(thread)
                    thread.start()
            except Exception as e:
                logger.error(str(e) + '  具体栈回溯信息查看crit.log  ')
                logger.exception(e)

            cpc_count = 0
            for l in thread_list:
                l.join()
                cpc_count += l.cpc_count

            logger.info('start_time: %d, cpc_count: %d' % (self.start_time, cpc_count))
            self.task.log((self.start_time, cpc_count))

    def run(self):

        logger.info('task start!!!')
        #self.gglm._init()

        thread_vector = self.thread_vector
        _len = len(thread_vector)

        try:
            while True:
                h, s = time.localtime()[3:5]
                if s == 0:
                    break
                else:
                    time.sleep(30)

            if h != 0:
                index = int(random.random() * _len)
                _thread_vector = thread_vector[index]
                for i, l in enumerate(_thread_vector[h:]):
                    l = l + int(random.random() * 10 - 5)
                    l = abs(l)
                    self.ControlThread(i + h, self, l)
                    time.sleep(3600)
                    if self.term_flag:
                        logger.info('接收到SIGTERM信号 退出....')
                        return

            while True:
                index = int(random.random() * _len)
                _thread_vector = thread_vector[index]
                #时间向量 保存一天24小时 每个小时需要运行的线程数量
                for i, l in enumerate(_thread_vector):
                    l = l + int(random.random() * 10 - 5)
                    l = abs(l)

                    # 如果今天是周六 周日 则需要提高浏览量
                    if int(time.strftime('%w')) in (6, 7):
                        l += 10

                    self.ControlThread(i, self, l)
                    time.sleep(3600)
                    if self.term_flag:
                        logger.info('接收到SIGTERM信号 退出....')
                        return

        except Exception as e:
            print e
            logger.exception(e)

    def signal_handler(self, signum, frame):
        if signum == signal.SIGTERM:
            self.term_flag = True
        else:
            pass

    def log(self, info):
        start_time = info[0]
        self.cpc_count += info[1]

        if start_time == 23:
            logger.info('24 hours, cpc_count: %d' % (self.cpc_count, ))
            self.cpc_count = 0


if __name__ == '__main__':
    task = Task()
    task.run()
