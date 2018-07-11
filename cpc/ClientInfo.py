#-*- coding: UTF-8 -*-

import sys
import cPickle as pickle
from VClient import *


reload(sys)
sys.setdefaultencoding('utf-8')


class ClientInfo(object):
    def __init__(self):
        self.root = pickle.load(open('client.dump', 'rb'))

    def get_client(self, platform=None):
        return self.root.get(platform)

    def get_info(self):
        return self.root.get_info()

    def dir(self, path):
        dir_list = reduce(lambda _list, elem: _list.append(elem) or _list if elem else _list, path.split('/'), list())
        layer = self.root
        for l in dir_list:
            layer = layer.children[l][0]
        layer.print_layer()


if __name__ == '__main__':
    from pprint import pprint
    ci = ClientInfo()
    ci.dir('/pc/win7')
    #pprint(ci.get_client(platform='mobile'))
    pprint(ci.get_client())
    #pprint(ci.get_info(), width=4)
