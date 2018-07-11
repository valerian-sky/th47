#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import random
import cPickle as pickle
from collections import OrderedDict
import logging


logger = logging.getLogger('task')
__all__ = ['layer', 'layer1', 'layer2', 'layer3', 'layer4']


reload(sys)
sys.setdefaultencoding('utf-8')


"""
get(name=None)  返回的结果result字典数据类型，其中包含的字段：

platform： pc：pc平台，mobile：移动
os： 操作系统
user_agent
accept
accept_language
accept_encoding
screen_size
color_depth
language
flash_version
browser
"""
class layer(object):
    def __init__(self, name, layer_num):
        self.name = name
        self.layer_num = layer_num
        self.total = 0
        self.probability = 0.0
        self.build_weight_flag = False
        self.children = {}

    def add(self, client):
        self.total += 1

        child_name = self.get_child_name(client)
        if self.children.get(child_name):
            self.children[child_name][1] += 1
            self.children[child_name][0].add(client)
            self.children[child_name][0].probability = float(self.children[child_name][0].total) / self.total
        else:
            self.children[child_name] = [self.get_child_layer()(child_name), 1]
            self.children[child_name][0].add(client)
            self.children[child_name][0].probability = float(self.children[child_name][0].total) / self.total

    def get_weighte_info(self):
        name = []
        weightes = []
        for k, v in self.children.items():
            name.append(k)
            weightes.append(float(v[1]) / self.total)

        return name, weightes

    def get(self, name=None):

        if not name:
            if self.build_weight_flag:
                index = self._weighted_choice_sub(self.weight_list)
                name = self.weight_list_name[index]
            else:
                name_list, weightes = self.get_weighte_info()
                index = self._weighted_choice_sub(weightes)
                name = name_list[index]

        return self.children[name][0].get()

    def print_layer(self):
        print 'name: %s' % self.name
        print 'layer_num: %d' % self.layer_num
        print 'total: %d' % self.total
        print 'children len: %d' % len(self.children)
        print 'probability: %f' % self.probability

        if self.layer_num == 4:
            print 'ua len: %d' % len(self.children)
            ll = []
            for k2 in self.children:
                n = self.children[k2]
                ll.append((k2, n['count'], len(n['accept']), len(n['accept_language']), len(n['accept_encoding'])))

            def _cmp(l1, l2):
                index1 = l1[1]
                index2 = l2[1]
                return cmp(int(index2), int(index1))

            ll.sort(cmp=_cmp)
            for l in ll:
                print '\t ua: %s, count: %d, accept_count: %d, accept_language: %d, accept_encoding: %d' % (l[0], l[1], l[2], l[3], l[4], )
        else:
            for k in self.children:
                print '\t name: %s, count: %d' % (k, self.children[k][1])

    def get_info(self):
        result = []
        d = OrderedDict()
        d['level'] = self.layer_num
        d['name'] = self.name
        d['total'] = self.total
        d['children'] = []
        for k, v in self.children.items():
            c = {}
            c['name'] = k
            c['nums'] = v[1]
            c['probability'] = float(v[1]) / self.total
            d['children'].append(c)

        d['children'].sort(key=lambda i: i['probability'])
        result.append(d)

        for v in self.children.values():
            result.extend(v[0].get_info())

        result.sort(key=lambda i: i['level'])
        return result

    def build_weight(self):
        if self.build_weight_flag:
            return

        _list = []
        for k in self.children:
            _list.append((k, float(self.children[k][1]) / self.total))

        _list.sort(key=lambda i: i[1], reverse=True)

        self.weight_list = []
        self.weight_list_name = []
        for l in _list:
            self.weight_list_name.append(l[0])
            self.weight_list.append(l[1])

        self.build_weight_flag = True

        for v in self.children.values():
            v[0].build_weight()

    @staticmethod
    def _weighted_choice_sub(weights):
        rnd = random.random() * sum(weights)
        for i, w in enumerate(weights):
            rnd -= w
            if rnd < 0:
                return i


#root层
class layer1(layer):
    def __init__(self, name):
        super(layer1, self).__init__(name, 1)

    def get_child_layer(self):
        return layer2

    def get_child_name(self, client):
        user_agent = client['user_agent'].lower()
        mobile_tag = ['android', 'iphone', 'ipad']
        pc_tag = ['windows nt', 'linux', 'macintosh']

        tag = filter(lambda i: i in user_agent, mobile_tag)
        if len(tag) > 1:
            raise ValueError((client['user_agent'], 'layer1'))

        tag2 = filter(lambda i: i in user_agent, pc_tag)
        if len(tag2) > 1:
            raise ValueError((client['user_agent'], 'layer1'))

        if tag:
            return 'mobile'
        elif tag2:
            return 'pc'
        else:
            raise ValueError((client['user_agent'], 'layer1'))


class layer2(layer):
    def __init__(self, name):
        super(layer2, self).__init__(name, 2)

    def get_child_layer(self):
        return layer3

    def get(self, name=None):
        client = super(layer2, self).get(name)
        client['platform'] = self.name
        return client

    def get_child_name(self, client):
        user_agent = client['user_agent'].lower()

        if 'windows nt 5.1' in user_agent:
            return 'winxp'
        elif 'windows nt 5.2' in user_agent:
            return 'win2003'
        elif 'windows nt 5.0' in user_agent:
            return 'win2000'
        elif 'windows nt 6.0' in user_agent:
            return 'vista'
        elif 'windows nt 6.1' in user_agent:
            return 'win7'
        elif 'windows nt 6.2' in user_agent:
            return 'win8'
        elif 'windows nt 6.3' in user_agent:
            return 'win8.1'
        elif 'windows nt 10' in user_agent:
            return 'win10'
        elif 'macintosh' in user_agent:
            return 'mac'
        elif 'android' in user_agent:
            return 'Android'
        elif 'iphone' in user_agent:
            return 'iphone'
        elif 'ipad' in user_agent:
            return 'ipad'
        elif 'linux' in user_agent:
            return 'linux'
        elif 'windows phone' in user_agent:
            return 'winphone'
        else:
            raise ValueError((client['user_agent'], 'layer2'))


class layer3(layer):
    def __init__(self, name):
        super(layer3, self).__init__(name, 3)

    def get_child_layer(self):
        return layer4

    def get(self, name=None):
        client = super(layer3, self).get(name)
        client['os'] = self.name
        return client

    def get_child_name(self, client):
        user_agent = client['user_agent'].lower()

        if 'firefox' in user_agent:
            return 'Firefox'
        elif '360se' in user_agent:
            return '360SE'
        elif '360ee' in user_agent:
            return '360EE'
        elif 'qqbrowser' in user_agent:
            return 'QQBrowser'
        elif 'metasr' in user_agent:
            return 'MetaSr'
        elif 'baidubrowser' in user_agent:
            return 'baidubrowser'
        elif 'maxthon' in user_agent:
            return 'Maxthon'
        elif 'opera' in user_agent:
            return 'Opera'
        elif 'Edge' in user_agent:
            return 'Edge'
        elif 'chrome' in user_agent:
            return 'Chrome'
        elif 'safari' in user_agent:
            return 'Safari'
        elif 'msie 10' in user_agent:
            return 'IE10'
        elif 'msie 9' in user_agent:
            return 'IE9'
        elif 'msie 8' in user_agent:
            return 'IE8'
        elif 'msie 7' in user_agent:
            return 'IE7'
        elif 'msie 6' in user_agent:
            return 'IE6'
        elif 'rv:' in user_agent:
            return 'ie11'

        elif 'ucbrowser' in user_agent:
            return 'UCBrowser'
        elif 'baiduboxapp' in user_agent:
            return 'BaiduBoxApp'
        elif 'sogoumobilebrowser' in user_agent:
            return 'SogouMobileBrowser'
        elif '14a456' in user_agent:
            return '14A456'
        elif 'ithunder' in user_agent:
            return 'iThunder'
        else:
            raise ValueError((client['user_agent'], 'layer3'))


# 叶子节点
class layer4(layer):
    def __init__(self, name):
        super(layer4, self).__init__(name, 4)
        self.other = {}
        self.other['screen_size'] = {}
        self.other['color_depth'] = {}
        self.other['language'] = {}
        self.other['flash_version'] = {}

        self.other['se'] = {}
        self.other['j'] = {}
        self.other['m'] = {}

    def build_weight(self):
        return

    def get_info(self):
        result = []
        d = OrderedDict()
        d['level'] = self.layer_num
        d['name'] = self.name
        d['total'] = self.total
        d['children_len'] = len(self.children)
        result.append(d)

        return result

    def add(self, client):
        user_agent = client['user_agent']
        self.total += 1

        if self.other['screen_size'].get(client['screen_size']):
            self.other['screen_size'][client['screen_size']] += 1
        else:
            self.other['screen_size'][client['screen_size']] = 1

        if self.other['color_depth'].get(client['color_depth']):
            self.other['color_depth'][client['color_depth']] += 1
        else:
            self.other['color_depth'][client['color_depth']] = 1

        if self.other['language'].get(client['language']):
            self.other['language'][client['language']] += 1
        else:
            self.other['language'][client['language']] = 1

        if self.other['flash_version'].get(client['flash_version']):
            self.other['flash_version'][client['flash_version']] += 1
        else:
            self.other['flash_version'][client['flash_version']] = 1

        if self.other['se'].get(client['se']):
            self.other['se'][client['se']] += 1
        else:
            self.other['se'][client['se']] = 1

        if self.other['j'].get(client['j']):
            self.other['j'][client['j']] += 1
        else:
            self.other['j'][client['j']] = 1

        if self.other['m'].get(client['m']):
            self.other['m'][client['m']] += 1
        else:
            self.other['m'][client['m']] = 1

        if not self.children.get(user_agent):
            if len(self.children) > 200:
                pass
            else:
                self.children[user_agent] = {}
                self.children[user_agent]['count'] = 0
                self.children[user_agent]['accept'] = {}
                self.children[user_agent]['accept_language'] = {}
                self.children[user_agent]['accept_encoding'] = {}

        if self.children.get(user_agent):
            d = self.children[user_agent]
            d['count'] += 1

            if client['accept'] not in d['accept'] and len(d['accept']) < 20:
                d['accept'][client['accept']] = 1
            elif client['accept'] in d['accept']:
                d['accept'][client['accept']] += 1
            else:
                print client['accept']

            if client['accept_language'] not in d['accept_language'] and len(d['accept_language']) < 20:
                d['accept_language'][client['accept_language']] = 1
            elif client['accept_language'] in d['accept_language']:
                d['accept_language'][client['accept_language']] += 1
            else:
                print client['accept_language']

            if client['accept_encoding'] not in d['accept_encoding'] and len(d['accept_encoding']) < 20:
                d['accept_encoding'][client['accept_encoding']] = 1
            elif client['accept_encoding'] in d['accept_encoding']:
                d['accept_encoding'][client['accept_encoding']] += 1
            else:
                print client['accept_encoding']

    def get_weighte_info(self, d):
        name = []
        weightes = []
        for k, v in d.items():
            name.append(k)
            if d == self.children:
                weightes.append(float(v['count']) / self.total)
            else:
                weightes.append(float(v) / self.total)

        return name, weightes

    def get(self):

        result = {}
        name, weightes = self.get_weighte_info(self.children)
        index = self._weighted_choice_sub(weightes)
        result['user_agent'] = name[index]
        d = self.children[name[index]]

        name, weightes = self.get_weighte_info(d['accept'])
        index = self._weighted_choice_sub(weightes)
        result['accept'] = name[index]

        name, weightes = self.get_weighte_info(d['accept_language'])
        index = self._weighted_choice_sub(weightes)
        result['accept_language'] = name[index]

        name, weightes = self.get_weighte_info(d['accept_encoding'])
        index = self._weighted_choice_sub(weightes)
        result['accept_encoding'] = name[index]

        name, weightes = self.get_weighte_info(self.other['screen_size'])
        index = self._weighted_choice_sub(weightes)
        result['screen_size'] = name[index]

        name, weightes = self.get_weighte_info(self.other['color_depth'])
        index = self._weighted_choice_sub(weightes)
        result['color_depth'] = name[index]

        name, weightes = self.get_weighte_info(self.other['language'])
        index = self._weighted_choice_sub(weightes)
        result['language'] = name[index]

        name, weightes = self.get_weighte_info(self.other['flash_version'])
        index = self._weighted_choice_sub(weightes)
        result['flash_version'] = name[index]
        result['browser'] = self.name

        name, weightes = self.get_weighte_info(self.other['se'])
        index = self._weighted_choice_sub(weightes)
        result['se'] = name[index]

        name, weightes = self.get_weighte_info(self.other['j'])
        index = self._weighted_choice_sub(weightes)
        result['j'] = name[index]

        name, weightes = self.get_weighte_info(self.other['m'])
        index = self._weighted_choice_sub(weightes)
        result['m'] = name[index]

        return result


def load(file_name):
    # d = globals()
    # print [k for k in d.keys() if 'layer' in k]
    # with open(file_name, 'rb') as f:
    #     root = pickle.loads(f.read())
    # locals().update(globals())
    # print locals()
    root = pickle.load(open(file_name, 'rb'))

    return root


def create_vclient():
    db = MyDB()
    db.init()

    try:
        root = pickle.load(open('client.dump', 'rb'))
    except IOError as e:
        print e
        root = layer1('root')

    try:
        count = pickle.load(open('count.dump', 'rb'))
    except IOError as e:
        print e
        count = 0

    _count = success_count = 0
    for l in db.get_client(count):
        d = {}
        d['user_agent'] = l[1]
        d['accept'] = l[2]
        d['accept_language'] = l[3]
        d['accept_encoding'] = l[4]
        d['language'] = l[5]
        d['platform'] = l[6]
        d['screen_size'] = l[7]
        d['flash_version'] = l[8]
        d['cookie_enable'] = l[9]
        d['color_depth'] = l[10]
        d['se'] = l[11]
        d['j'] = l[12]
        d['m'] = l[13]

        try:
            root.add(d)
            success_count += 1
        except ValueError as e:
            logger.error(str(e))
        except Exception as e:
            logger.error(str(e) + '  具体栈回溯信息查看crit.log')
            logger.exception(e)

        _count += 1
        count += 1

    logger.debug('_count: %s, success_count: %d' % (_count, success_count))

    #root.build_weight()
    with open('count.dump', 'wb') as f:
        f.write(pickle.dumps(count))

    with open('client.dump', 'wb') as f:
        f.write(pickle.dumps(root, True))

    db.close()


def create_vclient2():
    import ClientInfo2
    ci = ClientInfo2.ClientInfo()
    root = layer1('root')

    for i in range(20):
        d = {}
        client_info = ci.get_client('国内')
        d['user_agent'] = client_info['user_agent']
        d['screen_size'] = client_info['screen_size']
        d['accept'] = ['image/png,image/*;q=0.8,*/*;q=0.5', '*/*'][random.randint(0, 1)]
        d['accept_language'] = ['zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3', 'zh-CN'][random.randint(0, 1)]
        d['accept_encoding'] = 'gzip, deflate'
        d['language'] = client_info['lg']
        d['flash_version'] = ['21.0.0', '22.0.0', '20.0.0'][random.randint(0, 2)]
        d['platform'] = client_info['platform']
        d['cookie_enable'] = '1'
        d['color_depth'] = client_info['color_depth']
        root.add(d)

    root.build_weight()
    with open('client.dump', 'wb') as f:
        f.write(pickle.dumps(root, True))


if __name__ == '__main__':
    create_vclient()
    exit()

    root = layer1('root')
    d = {}
    d['user_agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
    d['screen_size'] = '1920x1080'
    d['accept'] = 'image/png,image/*;q=0.8,*/*;q=0.5'
    d['accept_language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    d['accept_encoding'] = 'gzip, deflate'
    d['language'] = 'zh-CN'
    d['flash_version'] = '21.0.0'
    d['platform'] = 'Win32'
    d['cookie_enable'] = '1'
    d['color_depth'] = '24'
    root.add(d)

    d = {}
    d['user_agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)'
    d['screen_size'] = '1920x1080'
    d['accept'] = 'application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*'
    d['accept_language'] = 'zh-CN'
    d['accept_encoding'] = 'gzip, deflate'
    d['language'] = 'zh-CN'
    d['flash_version'] = '22.0.0'
    d['platform'] = 'Win32'
    d['cookie_enable'] = '1'
    d['color_depth'] = '32'
    root.add(d)

    with open('client.dump', 'wb') as f:
        f.write(pickle.dumps(root, True))
