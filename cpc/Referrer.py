#-*- coding: UTF-8 -*-

import random
import time


g_referrer = {'pc': None, 'mobile': None}
g_referrer['pc'] = {'baidu': None, '360': None}

g_referrer['mobile'] = {'baidu': None, '360': None}
g_referrer['mobile']['baidu'] = {'m': None, 'm5': None, }


g_referrer['pc']['baidu'] = [
    ('https://www.baidu.com/link?url=%(url_hash)s&wd=&eqid=%(eqid)s', 24),
    ('http://www.baidu.com/s?wd=%(wd)s&tn=%(tn)s', 19),
    ('http://www.baidu.com/s?tn=%(tn)s&ch=2&ie=utf8&oe=utf8&wd=%(wd)s', 12),
    ('http://www.baidu.com/link?url=%(url_hash)s&wd=&eqid=%(eqid)s', 7),
    ('https://www.baidu.com/s?wd=%(wd)s&tn=%(tn)s&fenlei=mv6quAkxTZn0IZRqIHc1rHmYPjR0T1dBn1DdPhPWmW-9PycsmyP-0ZwV5HDYn1nvrjT0mv4YUWY4PH03n103rNqWTZc0TLPs5fK1TL0z5fKdThsqpZ', 3),
    ('http://www.baidu.com/s?ie=UTF-8&wd=%(wd)s', 1),
    ('http://www.baidu.com/s?ie=utf8&oe=utf8&wd=%(wd)s', 1),
    ('http://www.baidu.com/s?wd=%(wd)s&tn=%(tn)s&s2bd=t', 2),
    ('https://www.baidu.com', 2),
]
g_referrer['pc']['360'] = [
    ('http://www.haosou.com/s?q=%(wd)s&src=pdr_guide', 34),
    ('http://www.haosou.com/s?q=%(wd)s&src=recom-nlp-formal&from=recom-nlp-formal&resultFrom=recom-nlp', 14),
    ('http://www.haosou.com/s?ie=utf-8&shb=1&src=sug-store&q=%(wd)s', 15),
    ('http://www.haosou.com/s?ie=utf-8&shb=1&src=home_hao&q=%(wd)s', 3),
    ('http://www.haosou.com/s?ie=utf-8&shb=1&src=360se7_addr&q=%(wd)s', 2),
    ('http://www.haosou.com/s?ie=utf-8&q=%(wd)s', 2),
    ('http://www.haosou.com/s?q=%(wd)s&ie=utf-8&src=hao_360so', 10),
    ('http://www.haosou.com/link?url=%(url)s&q=%(wd)s&ts=%(ts)s&t=%(t)s&src=haosou', 21),
]
g_referrer['mobile']['baidu']['m'] = [
    ('http://m.baidu.com/from=%(from)s/bd_page_type=1/ssid=0/uid=0/baiduid=%(baiduid)s/w=0_10_%(wd)s/t=zbios/l=3/tc?ref=www_zbios&pu=%(pu)s', 98),
    ('http://m.baidu.com/s?from=%(from)s&word=%(wd)s', 1),
    ('http://m.baidu.com/s?from=%(from)s&bd_page_type=1&word=%(wd)s', 1),
]
g_referrer['mobile']['baidu']['m_iphone'] = [
    ('http://m.baidu.com/from=%(from)s/bd_page_type=1/ssid=0/uid=0/pu=%(pu)s/baiduid=%(baiduid)s/w=0_10_%(wd)s/t=iphone/l=3/tc?m=8&srd=1&dict=32&ti', 98),
    ('http://m.baidu.com/s?from=%(from)s&word=%(wd)s', 1),
    ('http://m.baidu.com/s?from=%(from)s&bd_page_type=1&word=%(wd)s', 1),
]
g_referrer['mobile']['baidu']['m5'] = [
    ('http://m5.baidu.com/s?from=124n&word=%(wd)s', 4),
]
g_referrer['mobile']['baidu']['m5_iphone'] = [
    ('http://m5.baidu.com/from=%(from)s/bd_page_type=1/ssid=0/uid=0/pu=%(pu)s/baiduid=%(baiduid)s/w=0_10_%(wd)s/t=iphone/l=3/tc?ref=www_iphone&lid=1', 95),
    ('http://m5.baidu.com/ssid=%(ssid)s/from=%(from)s/bd_page_type=1/uid=0/pu=%(pu)s/baiduid=%(baiduid)s/w=0_10_%(wd)s/t=iphone/l=3/tc?ref=www_iphone&lid=1', 1),
    ('http://m5.baidu.com/s?from=124n&word=%(wd)s', 4),
]
g_referrer['mobile']['360'] = [
    ('http://m.haosou.com/s?ie=utf-8&src=3600w&q=%(wd)s', 1),
    ('http://m.haosou.com/s?q=%(wd)s&src=suglist&srcg=360aphone&mso_from=360_browser', 1),
    ('http://m.haosou.com/index.php?ie=utf-8&src=hao_search&shb=1&hsid=2892c6c8634fe000&q=%(wd)s&a=index&ie=utf-8&src=hao_search&shb=1&hsid=2892c6c8634fe000&q=%(wd)s', 1),
    ('http://m.haosou.com/s?q=%(wd)s&src=360aphone_suglist&srcg=360aphone&version=6.9.9.22&category=internal&chl=h086669&user_id=e1de302b1715caf3fa316a0669a33c4e&poi_len=6&poi=1ir5EU0ExsBz8FEycFrirg==&tk=695e99a641a0e030ca4eba5390a9ef53&wid', 1),
    ('http://m.haosou.com/s?q=%(wd)s&src=360aphone_searchbar&srcg=zl_doyo_1&version=6.9.9.39&category=internal&chl=yz00058&user_id=536956696d87303fc89d8cf86e819be3&poi_len=31&poi=Bg3d3wJZp4qj8t0nDThUiBrYq0jvIN8nul0iKxhuSrw=&tk=cab8ba2323b2', 1),
    ('http://m.haosou.com/s?q=%(wd)s&src=360aphone_suglist&srcg=360aphone&version=6.9.9.39&category=internal&chl=900015&user_id=9890bdf42e0963a510ec1b2b7f91db11&poi_len=31&poi=sSAfkx6D9aEu6i6W8pryQ2kjTaHRIS4w0g45XaBMWUE=&tk=f778bb2bc0f05c0f', 1),
]


g_eqid = [
    'fba0fcaa000352ff0000000456790674',
    'ca5ccd8b000044780000000456793fc2',
    'ca5ccd8b000044780000000456793fc2',
    'ee5c3d70000006200000000456790773',
    '9c0a05000000177600000004567907d9',
    'ea0ad53100014efa000000025678d331',
    'd6c1e1600000a52e000000025673c84b',
    'ae57bc22000818550000000456786e9d',
    'e878e2ab0006e33f0000000356781b3b',
    '8715dae000023933000000025679847a',
    'dd613f1a0000a20f0000000256779bc8',
    'a739ae100004a123000000035678c1ec',
    'e3fc4f4c0001631500000003565aefdb',
    'dcb216bf00089a7b000000035677174d',
    'f30fb2070009f330000000035677226c',
    'd46fbbb800039d6d0000000356777f9e',
    'e3a9fdd90000a22d0000000356774829',
    '838c2c4c0000db3c0000000656775203',
    'c9e83e6e00003cd0000000035677686d',
    '8b92184200081f4b00000005567714b4',
    'eb6498be0001ba4f0000000356782f6a',
    'a6f3dbd70003f352000000035678bf5a',
]


g_tn = [
    '98050039_2_dg',
    '98010089_1_dg',
    '84053098_1_dg',
]


g_t = [
    'd06a1ad14d754e3ca7f64128ecb6b9c',
    'b34544d39e798ceca254f2c0deeb5ef',
    '612ef5cb0572e2ee351da97d9544882',
    '6debd74f9864d9e0d9aa78438debe70',
    '9721695a93ac9aca7ed15ae9e0aa556',
    '9c9e590eeed9075148811566a74904b',
    '17682bb4522dd097e7c982c2231a92c',
    'fc151fa109ebb876052f98a1e353b6f',
    '2abdf6f58d52ab17448d1c35f4dc38b',
    'f98fba8202f04c4de969e2d4f27d358',
    'a2acd2412a46e9644cf59c7073c4a62',
    '7bf230806dafa9dcee400f3cfa5e863',
    '62d9349331d5f49870164d176bc0088',
    'a2a9e284b23177940fc6e451af91d5b',
    '76bd85342060fe7fdc2004b11300e34',
    '933a70a159036f737da2e77c9385e6f',
    '53334ab5850a4a878f8bec701f66800',
    '54f405cfc6b78ada716105bc3289626',
    '68b4dda6d2903e8cd174036004a4a84',
    '0a51d86d69a38166304813c00c8516f',
    'd06a1ad14d754e3ca7f64128ecb6b9c',
    '8a14a71fc8647f01002586a8e171e7d',
]


g_from = [
    '1002253n',
    '7300001a',
    '1200a',
    '2001a',
    '1009928c',
    '1000943a',
    '1001560k',
    '1009395a',
    '1086k',
    '1099a',
    '1011986g',
    '1001187u',
    '7300001a',
    '1011267b',
    '1010888p',
    '1012852s',
    '1011279b',
    '1001560s',
    '1011813d',
]


g_pu = [
    'sz@1320_480,cuid@7BEB2C9DABE6C19B988FD49E',
    'sz@1320_480,cuid@laSca0ivvu0maHiXlP',
    'sz@1320_480,cuid@21A2A6CFFD4B493362ED315E3F949E1401248D2A4FRRCOEKLFS,cua@1242_2',
    'sz@1320_480,cuid@0a2JiguABi__aBiN_8vmi08ZSuja82tS',
    'sz@1320_480,cuid@1E0253ACC2A1403DBF274F4E23958E5E13A37AC14FRNFRJQCHQ,cua@750_13',
    'cuid@ju2Ga08RSilua2uwl82l8laFSilc8vi7_uBHf0ilviiFuvtg_u2Ki_aHB8gba2tHA,sz@1320_480,osname@baidubrowser,cua@_avLC_aE-i4qywoUfpw1zyaBXioeu-I4gN2w8AqqC,cut@_u2g8_uSvC_Uh2IJgNvHtyN',
    'sz@1320_480,cuid@0uv0a_u1Sa_9a-iu0avWa_8sSigZ8Bi5l8H9a_us2i8uu28Tga21i_uqBtjCa2tHA,cua@_avLC_aE-i4qywoUfpw1z4aBXi45a2iLA,cut@_u2g8_uSvC_Uh2IJgNvHtyNSmoi5pQqAC,osname@baiduboxapp,ctv@2,cfrom@1002037a,cen@cuid_cua_cut,csr',
]

g_pu_iphone = [
    'usm@0,sz@1320_2002,ta@iphone_1_9.0_2_6.1',
    'usm@0,sz@1320_1001,ta@iphone_2_4.1_3_534',
    'usm@0,sz@1320_1003,ta@iphone_2_4.4_1_10.4',
    'usm@0,sz@1320_1003,ta@iphone_2_5.0_1_10.9',
    'usm@0,sz@1320_1003,ta@iphone_2_4.4_1_10.9'
    'usm@0,sz@1320_1003,ta@iphone_2_4.4_1_10.8',
    'usm@0,sz@1320_1003,ta@iphone_2_4.4_1_10.7',
    'usm@0,sz@1320_1004,ta@iphone_2_4.4_11_2.0',
    'usm@0,sz@1320_1004,ta@iphone_2_4.2_11_1.0',
    'usm@0,sz@1320_1004,ta@iphone_2_5.0_11_2.1',
    'usm@0,sz@1320_2002,ta@iphone_1_6.1_2_6.1',
    'usm@0,sz@1320_1002,ta@iphone_2_4.4_2_6.3',
]

g_ssid = [
    'df81c0eebfad63630f78',
    'd075c9bdb6abcee4beaf374461',
    'ff81c0ecbaad63730f75',
]


class Referrer(object):
    def __init__(self):
        pass

    def url_hash(self):
        return 'url_hash'

    def url(self):
        return 'url'

    def key_word(self):
        return '超碰在线视频'

    def get_baiduid(self):
        baiduid = ''
        while True:
            c = random.choice('0123456789ABCDEF')
            baiduid += c
            if len(baiduid) == 32:
                break

        if baiduid[0] == '0':
            baiduid = 'D' + baiduid[1:]
        return baiduid

    def get_param(self):

        param = {}
        param['url_hash'] = self.url_hash()
        _len = len(g_eqid)
        index = int(random.random() * _len)
        param['eqid'] = g_eqid[index]
        param['wd'] = self.key_word()
        _len = len(g_tn)
        index = int(random.random() * _len)
        param['tn'] = g_tn[index]
        param['url'] = self.url
        _len = len(g_t)
        index = int(random.random() * _len)
        param['t'] = g_t[index]
        param['ts'] = str(int(time.time()))
        _len = len(g_from)
        index = int(random.random() * _len)
        param['from'] = g_from[index]
        if self.os == 'iPhone':
            _len = len(g_pu_iphone)
            index = int(random.random() * _len)
            param['pu'] = g_pu_iphone[index]
        else:
            _len = len(g_pu)
            index = int(random.random() * _len)
            param['pu'] = g_pu[index]
        param['baiduid'] = self.get_baiduid()
        _len = len(g_ssid)
        index = int(random.random() * _len)
        param['ssid'] = g_ssid[index]

        return param

    def get_search_referrer(self, url, platform, os):
        self.os = os
        self.url = url

        #不管是移动端还是PC端 百度为90% 360为10%
        se_weights = [9, 1]
        index = self._weighted_choice_sub(se_weights)

        #百度
        if index == 0:
            if platform == 'pc':
                referer_list = g_referrer['pc']['baidu']
            else:
                _weights = [0.99, 0.01]
                index = self._weighted_choice_sub(_weights)
                if index == 0:
                    if os == 'iPhone':
                        referer_list = g_referrer['mobile']['baidu']['m_iphone']
                    else:
                        referer_list = g_referrer['mobile']['baidu']['m']
                else:
                    if os == 'iPhone':
                        referer_list = g_referrer['mobile']['baidu']['m5_iphone']
                    else:
                        referer_list = g_referrer['mobile']['baidu']['m5']
        #360
        elif index == 1:
            referer_list = g_referrer[platform]['360']
        else:
            return ''

        if os == 'iPad':
            referer_list = [
                ('http://www.baidu.com/s?ie=utf-8&tn=%(tn)s&dsp=ipad&wd=%(wd)s', 13),
                ('http://www.baidu.com/s?ie=utf-8&tn=%(tn)s&dsp=ipad&wd=%(wd)s', 7),
            ]

        _weights = []
        for l in referer_list:
            _weights.append(l[1])

        index = self._weighted_choice_sub(_weights)
        referer = referer_list[index]
        referer = referer[0] % self.get_param()
        #referer = urllib.quote(referer, '?:/&=,')

        if 'www.baidu' in referer:
            referer = referer[:255]
        elif 'm.baidu' in referer:
            referer = referer[:251]
        elif 'm5.baidu' in referer:
            referer = referer[:251]

        return referer

    def _weighted_choice_sub(self, weights):
            rnd = random.random() * sum(weights)
            for i, w in enumerate(weights):
                rnd -= w
                if rnd < 0:
                    return i


if __name__ == '__main__':

    rf = Referrer()
    while True:
        referer = rf.get_search_referrer()
        print referer
