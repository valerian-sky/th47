#-*- coding: UTF-8 -*-

import sys
import time
import threading
import socket
import pickle
import random
import Queue
import logging
from MyCurl import MyCurl


reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger('task')


g_total_ip = 0
g_full_times = 0
g_empty_times = 0
g_server_ip = '45.118.132.145'
g_server_port = 12348

#用户ip区域及权重
g_ip_zone = [
    ('北京', 7),
    ('上海', 8),
    ('天津', 4),
    ('重庆', 3),

    ('内蒙古', 1),
    ('宁夏', 1),
    ('新疆', 1),
    ('西藏', 1),
    ('广西', 2),

    ('黑龙江', 2),
    ('吉林', 1),
    ('辽宁', 2),
    ('江苏', 6),
    ('山东', 4),
    ('安徽', 5),
    ('河北', 3),
    ('河南', 2),
    ('湖北', 2),
    ('湖南', 2),
    ('江西', 3),
    ('陕西', 1),
    ('山西', 2),
    ('四川', 3),
    ('青海', 1),
    ('海南', 2),
    ('广东', 8),
    ('贵州', 3),
    ('浙江', 8),
    ('福建', 7),
    ('甘肃', 1),
    ('云南', 4),

    ('香港', 4),

    ('台湾', 4),
    #('日本', 2),
    #('韩国', 1),
    #('美国', 4),
    #('国外', 3),
]


g_proxy_ip = []
g_lock = threading.Lock()
def get_proxy_ip(ip_zone):
    global g_proxy_ip

    g_lock.acquire()
    if g_proxy_ip:
        proxy_ip = g_proxy_ip.pop()
        g_lock.release()
        return proxy_ip

    mc = MyCurl()
    url = 'http://tpv.daxiangdaili.com/ip/?tid=556436807161584&num=30&category=2&foreign=none&filter=on'

    num = 0
    while True:
        try:
            info, proxy_ip_list = mc.get(url)
        except Exception as e:
            if num > 2:
                #print self.ip_zone, e
                g_lock.release()
                return ''
            else:
                num += 1
                continue
        else:
            if info['http-code'] == 503:
                #time.sleep(int(random.random() * 10))
                time.sleep(3)
                continue
            else:
                break
        finally:
            pass
            #g_lock.release()

    if '没有找到符合条件的IP' in proxy_ip_list:
        #print ('没有找到符合条件的IP %s' % self.ip_zone).decode('utf-8')
        g_lock.release()
        return get_proxy_ip2(ip_zone)

    if '订单剩余数量不足' in proxy_ip_list:
        #print ('订单剩余数量不足')
        g_lock.release()
        return get_proxy_ip2(ip_zone) 

    if '订单已经过期' in proxy_ip_list:
        #print ('订单已经过期')
        g_lock.release()
        return get_proxy_ip2(ip_zone)

    proxy_ip_list = proxy_ip_list.split('\r\n')
    g_proxy_ip = proxy_ip_list
    if g_proxy_ip:
        #print g_proxy_ip, len(g_proxy_ip)
        r =  g_proxy_ip.pop()
    else:
        r = ''

    g_lock.release()
    return r


g_proxy_ip2 = []
g_lock2 = threading.Lock()
def get_proxy_ip2(ip_zone):
    global g_proxy_ip2

    g_lock2.acquire()
    if g_proxy_ip2:
        proxy_ip = g_proxy_ip2.pop()
        g_lock2.release()
        return proxy_ip

    mc = MyCurl()
    url = 'http://tpv.daxiangdaili.com/ip/?tid=556436807161584&num=100&foreign=none&filter=on'

    num = 0
    while True:
        try:
            info, proxy_ip_list = mc.get(url)
        except Exception as e:
            if num > 2:
                #print self.ip_zone, e
                g_lock2.release()
                return ''
            else:
                num += 1
                continue
        else:
            if info['http-code'] == 503:
                time.sleep(int(random.random() * 10))
                continue
            else:
                break

    if '没有找到符合条件的IP' in proxy_ip_list:
        #print ('没有找到符合条件的IP %s' % self.ip_zone).decode('utf-8')
        g_lock2.release()
        return get_proxy_ip3(ip_zone)

    if '订单剩余数量不足' in proxy_ip_list:
        #print ('订单剩余数量不足')
        g_lock2.release()
        return ''

    if '订单已经过期' in proxy_ip_list:
        #print ('订单已经过期')
        g_lock2.release()
        return ''

    proxy_ip_list = proxy_ip_list.split('\r\n')
    g_proxy_ip2 = proxy_ip_list
    if g_proxy_ip2:
        #print g_proxy_ip2, len(g_proxy_ip2)
        r =  g_proxy_ip2.pop()
    else:
        r = ''

    g_lock2.release()
    return r


g_proxy_ip3 = []
g_lock3 = threading.Lock()
def get_proxy_ip3(ip_zone):
    global g_proxy_ip3

    g_lock3.acquire()
    if g_proxy_ip3:
        proxy_ip = g_proxy_ip3.pop()
        g_lock3.release()
        return proxy_ip

    mc = MyCurl()
    url = 'http://tpv.daxiangdaili.com/ip/?tid=556436807161584&num=100&foreign=none'

    num = 0
    while True:
        try:
            info, proxy_ip_list = mc.get(url)
        except Exception as e:
            if num > 2:
                #print self.ip_zone, e
                g_lock3.release()
                return ''
            else:
                num += 1
                continue
        else:
            if info['http-code'] == 503:
                time.sleep(int(random.random() * 10))
                continue
            else:
                break

    if '没有找到符合条件的IP' in proxy_ip_list:
        #print ('没有找到符合条件的IP %s' % self.ip_zone).decode('utf-8')
        g_lock3.release()
        return ''

    if '订单剩余数量不足' in proxy_ip_list:
        g_lock3.release()
        return ''

    if '订单已经过期' in proxy_ip_list:
        g_lock3.release()
        return ''

    proxy_ip_list = proxy_ip_list.split('\r\n')
    g_proxy_ip3 = proxy_ip_list
    if g_proxy_ip3:
        r = g_proxy_ip3.pop()
    else:
        r = ''

    g_lock3.release()
    return r


class ProxyIpClient(object):
    def __init__(self):
        global g_ip_zone

        self.term_flag = False
        self.proxy_ip_info = {}
        self.proxy_ip_info['proxy_ip'] = {}
        for l in g_ip_zone:
            self.proxy_ip_info['proxy_ip'][l[0]] = {}
            self.proxy_ip_info['proxy_ip'][l[0]]['limit'] = 10
            self.proxy_ip_info['proxy_ip'][l[0]]['queue'] = Queue.Queue(10)

        self.lock = threading.Lock()

        self._init()

    def _init(self):
        logger.info('task start!!!')
        self.WorkThread(self)
        self.DebugThread(self)

    class DebugThread(threading.Thread):
        def __init__(self, proxy_client):
            super(type(self), self).__init__()
            self.proxy_client = proxy_client
            self.setDaemon(True)
            self.start()

        def run(self):
            global g_full_times
            global g_empty_times
            global g_total_ip
            h = -1

            while True:
                _log_info = []
                current_total = 0
                for k in self.proxy_client.proxy_ip_info['proxy_ip']:
                    _len = self.proxy_client.proxy_ip_info['proxy_ip'][k]['queue'].qsize()
                    _log_info.append((k, _len))
                    current_total += _len

                _log = ''
                for j in _log_info:
                    _log += j[0] + ': ' + str(j[1]) + ', '
                logger.debug(_log)

                logger.debug('g_full_times: %d, g_empty_times: %d, g_total_ip: %d, current_total: %d' % (g_full_times, g_empty_times, g_total_ip, current_total))

                _h = time.localtime()[3]
                if _h == 0 and h == 23:
                    g_full_times = 0
                    g_empty_times = 0
                    g_total_ip = 0
                h = _h

                time.sleep(60)

    class WorkThread(threading.Thread):
        def __init__(self, proxy_client):
            super(type(self), self).__init__()
            self.proxy_client = proxy_client
            self.setDaemon(True)
            self.start()

        def reconnect(self):
            fd = socket.socket()
            while True:
                try:
                    fd.connect((g_server_ip, g_server_port))
                except Exception as e:
                    logger.error(str(e) + '  具体栈回溯信息查看crit.log  ')
                    logger.exception(e)
                    time.sleep(30)
                    continue
                else:
                    break

            return fd

        def recv(self, fd):
            result = fd.recv(10)
            if not result:
                fd.close()
                fd = self.reconnect()
                return self.recv(fd)
            data_len = int(result)

            result = ''
            while True:
                _data = fd.recv(data_len)
                if not _data:
                    fd.close()
                    fd = self.reconnect()
                    return self.recv(fd)
                result += _data
                if len(result) == data_len:
                    break

            return result

        def run(self):
            global g_full_times
            global g_total_ip
            logger.info('WorkThread start!!!')

            fd = self.reconnect()

            try:
                while True:

                    try:
                        result = self.recv(fd)
                    except Exception as e:
                        logger.error(str(e) + '  具体栈回溯信息查看crit.log  ')
                        logger.exception(e)
                        fd.close()
                        fd = self.reconnect()
                        continue

                    proxy_ip_list = pickle.loads(result)
                    #_log_info = []
                    for l in proxy_ip_list:
                        ip_zone = l[0]
                        zone_ip_list = l[1]
                        g_total_ip += len(zone_ip_list)
                        #print ip_zone, zone_ip_list
                        #_log_info.append((ip_zone, len(zone_ip_list)))
                        queue = self.proxy_client.proxy_ip_info['proxy_ip'][ip_zone]['queue']
                        for i in zone_ip_list:
                            #limit = self.proxy_client.proxy_ip_info['proxy_ip'][ip_zone]['limit']
                            #_len = queue.qsize()
                            try:
                                queue.put(i, False)
                            except:
                                #print ip_zone, 'full'
                                #logger.info('%s queue full' % ip_zone)
                                queue_size = queue.qsize()
                                if queue_size > 100:
                                    g_full_times += 1
                                    queue.get()
                                    queue.put(i, False)
                                else:
                                    self.proxy_client.lock.acquire()
                                    _len = int(queue_size * 1.3)
                                    new_queue = Queue.LifoQueue(_len)
                                    while True:
                                        try:
                                            ip = queue.get(False)
                                            new_queue.put(ip, False)
                                        except Queue.Empty as e:
                                            break
                                        except:
                                            self.proxy_client.lock.release()
                                            raise
                                    new_queue.put(i, False)
                                    self.proxy_client.proxy_ip_info['proxy_ip'][ip_zone]['queue'] = new_queue
                                    queue = new_queue
                                    self.proxy_client.lock.release()

                    #print g_total_ip, g_full_times
                    #logger.debug('g_total_ip: %d, g_full_times: %d' % (g_total_ip, g_full_times))
                    # _log = ''
                    # for j in _log_info:
                    #     _log += j[0] + ': ' + str(j[1]) + ', '
                    #logger.debug(_log)
                    #print
            except Exception as e:
                logger.error('result: %s len: %d' % (result, len(result)))
                logger.error(str(e) + '  具体栈回溯信息查看crit.log  ')
                logger.exception(e)

    def get_proxy_ip(self, ip_zone):
        global g_empty_times

        if ip_zone:
            try:
                queue = self.proxy_ip_info['proxy_ip'][ip_zone]['queue']
            except:
                return ''

            try:
                ip = queue.get(False)
            except Queue.Empty as e:
                print ip_zone, 'empty'
            except Exception as e:
                logger.error(str(e) + '  具体栈回溯信息查看crit.log  ')
                logger.exception(e)
                return ''
            else:
                return ip

        self.lock.acquire()
        _k_list = []
        for k in self.proxy_ip_info['proxy_ip']:
            if self.proxy_ip_info['proxy_ip'][k]['queue'].qsize() > 0:
                _k_list.append(k)

        _len = len(_k_list)
        if _len:
            index = int(random.random() * _len)
            k = _k_list[index]
            ip = self.proxy_ip_info['proxy_ip'][k]['queue'].get()
            self.lock.release()
            return ip
        else:
            self.lock.release()
            g_empty_times += 1
            return ''

    def info(self):
        for k in self.proxy_ip_info['proxy_ip']:
            _len = self.proxy_ip_info['proxy_ip'][k]['queue'].qsize()
            print k, _len
        print


if __name__ == '__main__':
    while True:
        print get_proxy_ip('')
        time.sleep(5)
