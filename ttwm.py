#-*- coding: UTF-8 -*-

import sys
import time
import urllib
import random
import logging
import base64
import re
import json
import gzip
import StringIO
from cpc.MyCurl import MyCurl
from cpc import ClientInfo
from cpc import ProxyIpClient
from cpc.VClient import *


reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger('task')


g_ci = ClientInfo.ClientInfo()


class EmptyProxyIpError(Exception):
    pass


class TTWM(object):
    def __init__(self):
        self.cpc_count = 0

    def get_click_referrer(self):

        url = [
            ('http://e.teamblog.jp/', 10),
            ('http://wear.tk/', 9),
            ('http://road.ga/', 8),
            ('http://give.ga/', 7),
            ('http://coat.cf/', 6),
            ('http://with.gq/', 5),
            ('http://fuli.droppages.com/', 4),
            ('http://hand.gq/', 3),
            ('http://dear.gq/', 2),
            ('http://www.haoavdh.com/', 2),
            ('http://boat.ml/', 3),
            ('http://74fuli.net/', 2),
            ('http://what.gq/', 1),
            ('http://y.1668.info/', 1),
            ('http://ripe.ml/', 1),
            ('http://landh.ga/', 1),
            ('http://ccde.tk/', 1),
            ('http://stop.401bus.com/', 1),
            ('http://selang.ga/', 1),
        ]

        _weights = []
        for l in url:
            _weights.append(l[1])
        index = self._weighted_choice_sub(_weights)

        return url[index][0]

    def _init(self):
        global g_ci

        client = g_ci.get_client('mobile')

        screen = client['screen_size']
        self.screen_width = screen.split('x')[0]
        self.screen_height = screen.split('x')[1]
        self.lang = client['language']
        self.cookie_enable = '1'
        self.os = client['os']
        self.platform = client['platform']
        self.browser = client['browser']
        self.color_depth = client['color_depth']
        self.user_agent = client['user_agent']
        self.flash_version = client['flash_version']
        self.accept = client['accept']
        self.accept_encoding = client['accept_encoding']
        self.accept_language = client['accept_language']
        self.se = client['se']
        self.j = client['j']
        self.m = client['m']
        self.h = str(int(0.83 * int(self.screen_height)))

        if random.random() < 0.8:
            self.url = 'http://th47.net/forum.php'
            self.domain = 'th47.net'
        else:
            self.url = 'http://taohua47.com/forum.php'
            self.domain = 'taohua47.com'

        weights = [1, 1, 8]
        index = self._weighted_choice_sub(weights)
        if index == 0:
            self.referrer = ''
        elif index == 1:
            self.referrer = ''
        else:
            self.referrer = self.get_click_referrer()

    def gzdecode(self, data):
        compressedstream = StringIO.StringIO(data)
        gziper = gzip.GzipFile(fileobj=compressedstream)

        try:
            data2 = gziper.read()
        except:
            return data

        return data2

    def reset_proxy_ip(self, status='not_click'):

        if status == 'click':
            get_proxy_ip = ProxyIpClient.get_proxy_ip
        else:
            get_proxy_ip = ProxyIpClient.get_proxy_ip2

        _count = 0
        while True:
            _proxy_ip = get_proxy_ip('')
            if _proxy_ip:
                break
            else:
                if _count > 3:
                    raise EmptyProxyIpError('没有足够代理ip %s' % status)
                else:
                    _count += 1
                    time.sleep(3)

        print 'proxy_ip: %s' % _proxy_ip
        self.proxy_mc = MyCurl(cookie_file_path='', proxy_ip=_proxy_ip, accept=self.accept, accept_language=self.accept_language, \
            accept_encoding=self.accept_encoding, user_agent=self.user_agent)

    def get_click_xy(self):
        width = int(self.screen_width)
        height = 100

        choise_weighted = [0.1, 10, 30, 50, 30, 10, 0.1]

        _len = len(choise_weighted)
        index = self._weighted_choice_sub(choise_weighted)
        size = width / _len
        x1 = index * size
        x2 = x1 + size
        x = random.randint(x1 + 5, x2 - 5)

        size = height / _len
        y1 = index * size
        y2 = y1 + size
        y = random.randint(y1 + 5, y2 - 5)

        return x, y

    def start(self, _d=None):

        self._init()

        weights = [7, 3]
        index = self._weighted_choice_sub(weights)
        if index == 0:
            click_flag = False
            self.reset_proxy_ip('not_click')
        else:
            click_flag = True
            self.reset_proxy_ip('click')

        p = [
            ('j', urllib.quote_plus(self.j)),
            ('m', urllib.quote_plus(self.m)),
            ('f', urllib.quote_plus(self.flash_version)),
            ('r', urllib.quote_plus(self.referrer)),
            ('u', urllib.quote_plus(self.url)),
            ('res', urllib.quote_plus(self.screen_width + 'x' + self.screen_height)),
            ('t', urllib.quote('淘花社区 - 手机版')),
            ('l', urllib.quote_plus(self.lang)),
            ('c', urllib.quote_plus(self.cookie_enable)),
            ('h', urllib.quote_plus(self.h)),
            ('se', urllib.quote_plus(self.se))
        ]

        p = '&'.join([l[0] + '=' + l[1] for l in p])

        arg = [
            ("siteid", ''),
            ("id", '58'),
            ("p", base64.b64encode(p)),
            ("l", base64.b64encode(self.domain)),
        ]

        arg = '&'.join([l[0] + '=' + l[1] for l in arg])

        url = 'http://js.7jiajiao.com/v.php?' + arg
        print url, self.url

        execute_count = 0
        t = time.time()
        while True:
            try:
                info, result = self.proxy_mc.get(url, referer=self.url)
            except Exception as e:
                print e
                try:
                    if click_flag:
                        self.reset_proxy_ip('click')
                    else:
                        self.reset_proxy_ip('not_click')
                except Exception as e:
                    logger.error(str(e) + '  具体栈回溯信息查看crit.log  ')
                    logger.exception(e)
                    return
                else:
                    execute_count += 1
                    if execute_count < 8:
                        continue
                    else:
                        logger.info('execute_count == 8')
                        return
            else:
                result = self.gzdecode(result)
                if 'var ads' not in result:
                    print 'dont have var ads'
                    logger.debug('dont have var ads')
                    if click_flag:
                        self.reset_proxy_ip('click')
                    else:
                        self.reset_proxy_ip('not_click')
                    continue
                break

        ads = re.search(r'var ads = (\[.*?\]);', result).group(1)
        ads = json.loads(ads)
        _url = ads[0]['url'].encode('utf-8')

        st = int(time.time() - t)
        st2 = random.randint(10, 50)
        if st < st2:
            time.sleep(st2 - st)

        if click_flag:
            x, y = self.get_click_xy()
            b = '&b=' + str(x) + ';' + str(y)
            g = '&g=' + str(x) + ';' + str(y)
            _url = _url + b + g

            print _url, url
            try:
                self.proxy_mc.get(_url, referer=url)
            except Exception as e:
                print e
            else:
                self.cpc_count += 1

    def _weighted_choice_sub(self, weights):
        rnd = random.random() * sum(weights)
        for i, w in enumerate(weights):
            rnd -= w
            if rnd < 0:
                return i


if __name__ == '__main__':
    obj = TTWM()
    obj.start()
