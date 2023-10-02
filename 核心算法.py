import json
import warnings

import requests
import re
from urllib import parse
import time

from wxpusher import WxPusher

from jd.tools import utils
from jd.tools.jd_sign import getSign

warnings.filterwarnings('ignore')
 

def getUrlParams(url):
    res = dict(parse.parse_qsl(url))
    return res


def get_cookie_string(cookie):
    cookie_string = ''
    for cookie_key in cookie.keys():
        cookie_string += '%s=%s;' % (cookie_key, cookie[cookie_key])
    return cookie_string


def get_jd_time():
    response = requests.get(url='https://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5')
    print(response.json())


def get_sk(data):
    data_val = [val for val in data['data'].values()]
    n, o, p, q, r, s = data_val[0], data_val[1], data_val[2], data_val[3], data_val[4], data_val[5]
    sk_val = ''
    if n == 'cca':
        sk_val = p[14:19].lower() + o[5:15].upper()
    if n == 'ab':  # check ok
        sk_val = r[10:18] + s[2:13].lower()
    if n == 'ch':
        sk_val = q.upper() + r[6:10].upper()
    if n == 'cbc':  # check ok
        sk_val = q[3:13].upper() + p[10:19].lower()
    if n == 'by':
        sk_val = o[5:8] + re.sub('a', 'c', p, flags=re.IGNORECASE)
    if n == 'xa':
        sk_val = o[1:16] + s[4:10]
    if n == 'cza':
        sk_val = q[6:19].lower() + s[5:11]
    if n == 'cb':
        sk_val = s[5:14] + p[2:13].upper()

    return sk_val


class JDSecKillAPI:
    def __init__(self, sku, ck):
        self.skuId = sku
        self.s = requests.session()
        self.sku = sku
        self.ck = ck
        self.aid = ''
        self.eid = 'eidAccfa8121das3mOM5swaGRcSw7E22kO50H5jjOzSUZLdxjWFZLi3ATsvj875K/RWM0W4ztxrbes6TNeio5uhWCeJIKObRbFo6NaYRyMqYuMJ2MM5D'
        self.uuid = '351792042184702-6dd3f46ae26a'
        self.uts = '0f31TVRjBSsqndu4/jgUPz6uymy50MQJAUhDDPnNIByQiRdjk5SK6CXmdShdxGaPRUd2+o8JNufp2fsgzyZpKhao+6lXsd3TXF8+jFmN/08eWFOjD36AXn3DPYPoc8MKL9ccf40wpTgO1wSP1oliin/fcMzzPHSxzINfo/svdCXHzPsMY3eZLWP0KGqPLr5fXA1RZRoBs4xl/IYv7E80OQ=='
        self.wifiBssid = ''
        # self.ua = 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36'
        self.ua = 'Mozilla/5.0 (Linux; Android 12; 22021211RC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046011 Mobile Safari/537.36'

    def appoint_sku(self):
        headers = {
            'user-agent': 'okhttp/3.12.1;jdmall;android;version/10.5.0;build/95837;',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': self.ck,
            'jdc-backup': self.ck,
        }

        ts = int(time.time() * 1000)
        uuid = self.uuid
        ep = utils.get_ep(ts, uuid)

        query_params = {
            'functionId': 'appoint',
            'clientVersion': '10.5.0',
            'build': '95837',
            'client': 'android',
            'd_brand': 'HUAWEI',
            'd_model': 'LIO-AN00',
            'osVersion': '7.1.2',
            'screen': '1920*1080',
            'partner': 'hhqj02',
            'aid': self.aid,
            'eid': self.eid,
            'sdkVersion': '29',
            'lang': 'zh_CN',
            'harmonyOs': '0',
            'uuid': self.uuid,
            'area': '',
            'networkType': 'wifi',
            'wifiBssid': self.wifiBssid,
            'uts': self.uts,
            'uemps': '0-0',
            'ext': '{"prstate":"0","pvcStu":"1"}',
            'ef': '1',
            'ep': json.dumps(ep, ensure_ascii=False, separators=(',', ':')),
        }
        reserve_url = 'https://api.m.jd.com/client.action'

        body = {"autoAddCart": "0", "bsid": "", "check": "0", "ctext": "", "isShowCode": "0", "mad": "0",
                "skuId": self.skuId, "type": "1"}

        plainTextDic = {
            "st": ts,  # 毫秒级时间戳
            "sv": "120",
            "functionId": query_params['functionId'],
            "uuid": uuid,
            "client": query_params['client'],
            "clientVersion": query_params['clientVersion'],
            "body": json.dumps(body, ensure_ascii=False, separators=(',', ':'))
        }
        st, sign, sv = getSign(plainTextDic)

        query_params.update(st=st)
        query_params.update(sign=sign)
        query_params.update(sv=sv)

        data = {'body': json.dumps(body, ensure_ascii=False, separators=(',', ':'))}

        response = self.s.post(url=reserve_url,
                               params=query_params,
                               data=data,
                               headers=headers,
                               allow_redirects=False,
                               verify=False,
                               timeout=3)
        return response.json()

    def get_token_key(self):
        headers = {
            'user-agent': 'okhttp/3.12.1;jdmall;android;version/10.5.0;build/95837;',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': self.ck,
            'jdc-backup': self.ck,
        }

        ts = int(time.time() * 1000)
        uuid = self.uuid
        ep = utils.get_ep(ts, uuid)

        query_params = {
            'functionId': 'genToken',
            'clientVersion': '10.5.0',
            'build': '95837',
            'client': 'android',
            'd_brand': 'HUAWEI',
            'd_model': 'LIO-AN00',
            'osVersion': '7.1.2',
            'screen': '1920*1080',
            'partner': 'hhqj02',
            'aid': self.aid,
            'eid': self.eid,
            'sdkVersion': '29',
            'lang': 'zh_CN',
            'harmonyOs': '0',
            'uuid': self.uuid,
            'area': '',
            'networkType': 'wifi',
            'wifiBssid': self.wifiBssid,
            'uts': self.uts,
            'uemps': '0-0',
            'ext': '{"prstate":"0","pvcStu":"1"}',
            'ef': '1',
            'ep': json.dumps(ep, ensure_ascii=False, separators=(',', ':')),
        }

        body = {"action": "to", "to": "https://divide.jd.com/user_routing?skuId="+self.sku}

        plainTextDic = {
            "st": ts,  # 毫秒级时间戳
            "sv": "120",
            "functionId": query_params['functionId'],
            "uuid": uuid,
            "client": query_params['client'],
            "clientVersion": query_params['clientVersion'],
            "body": json.dumps(body, ensure_ascii=False, separators=(',', ':'))
        }
        st, sign, sv = getSign(plainTextDic)

        query_params.update(st=st)
        query_params.update(sign=sign)
        query_params.update(sv=sv)

        data = {'body': json.dumps(body, ensure_ascii=False, separators=(',', ':'))}

        response = self.s.post(url='https://api.m.jd.com/client.action',
                               params=query_params,
                               data=data,
                               headers=headers,
                               allow_redirects=False,
                               verify=False,
                               timeout=3)
        # token_key = response.json()['tokenKey']
        # print('Token Key: ----------> %s' % response.json())
        # print(response.status_code)
        json_obj = response.json()
        print('Get genToken--------------->%s' % str(json_obj))
        return json_obj

    def get_appjmp(self, token_params):
        headers = {
            'user-agent': self.ua
        }
        appjmp_url = token_params['url']
        params = {
            'to': 'https://divide.jd.com/user_routing?skuId=%s' % self.skuId,
            'tokenKey': token_params['tokenKey']
        }

        response = self.s.get(url=appjmp_url, params=params, allow_redirects=False, verify=False, headers=headers)
        print('Get Appjmp跳转链接-------------->%s' % response.headers['Location'])
        return response.headers['Location']

    def get_divide(self, divide_url):
        headers = {
            'user-agent': self.ua
        }
        response = self.s.get(url=divide_url, allow_redirects=False, verify=False, headers=headers)
        print('Get Divide跳转链接-------------->%s' % response.headers['Location'])
        return response.headers['Location']

    def get_captcha(self, captcha_url):
        headers = {
            'user-agent': self.ua
        }
        response = self.s.get(url=captcha_url, allow_redirects=False, verify=False, headers=headers)
        print('Get Captcha跳转链接-------------->%s' % response.headers['Location'])
        return response.headers['Location']

    def visit_seckill(self, seckill_url):
        headers = {
            'user-agent': self.ua
        }
        response = self.s.get(url=seckill_url, allow_redirects=False, verify=False, headers=headers)
        return response

    def init_action(self, num=1):

        try:
            headers = {
                'user-agent': self.ua,
                'Connection': 'keep-alive'
            }
            init_action_url = 'https://marathon.jd.com/seckillnew/orderService/init.action'
            data = {
                'sku': self.skuId,
                'num': num,
                'id': 0,
                'provinceId': 0,
                'cityId': 0,
                'countyId': 0,
                'townId': 0,
            }
            response = self.s.post(url=init_action_url, data=data, allow_redirects=False, verify=False, headers=headers)
            print('init action返回数据：%s' % response.text)
            return response.json()
        except Exception as e:
            print(str(e))
            return None


    def get_tak(self):
        try:
            headers = {
                'user-agent': self.ua,
                'Connection': 'keep-alive'
            }
            tak_url = 'https://tak.jd.com/t/871A9?_t=%d' % (int(round(time.time() * 1000)))
            response = self.s.get(url=tak_url, allow_redirects=False, verify=False, headers=headers)
            sk_val = get_sk(data=response.json())
            return sk_val
        except Exception as e:
            #print(str(e))
            return ''

    def submit_order(self, order_data, sk):
        try:
            headers = {
                'user-agent': self.ua,
                'Connection': 'keep-alive'
            }
            submit_order_url = 'https://marathon.jd.com/seckillnew/orderService/submitOrder.action?skuId=%s' % self.skuId
            address_info = order_data['address']
            invoice_info = order_data['invoiceInfo']
            data = {
                'num': order_data['seckillSkuVO']['num'],
                'addressId': address_info['id'],
                'yuShou': True,
                'isModifyAddress': False,
                'name': address_info['name'],
                'provinceId': address_info['provinceId'],
                'provinceName': address_info['provinceName'],
                'cityId': address_info['cityId'],
                'cityName': address_info['cityName'],
                'countyId': address_info['countyId'],
                'countyName': address_info['countyName'],
                'townId': address_info['townId'],
                'townName': address_info['townName'],
                'addressDetail': address_info['addressDetail'],
                'mobile': address_info['mobile'],
                'mobileKey': address_info['mobileKey'],
                'email': '',
                'invoiceTitle': invoice_info['invoiceTitle'],
                'invoiceContent': invoice_info['invoiceContentType'],
                'invoicePhone': invoice_info['invoicePhone'],
                'invoicePhoneKey': invoice_info['invoicePhoneKey'],
                'invoice': True,
                'codTimeType': '3',
                'paymentType': '4',
                'overseas': '0',
                'token': order_data['token'],
                'sk': sk,
            }

            response = self.s.post(url=submit_order_url, data=data, allow_redirects=False, verify=False, headers=headers)
            return response.json()
        except Exception as e:
            print('submit error--->')
            return None

    def send_message(self, content):
        try:
            # 推送token
            PUSH_TOKEN = 'AT_4XxUFvSjSLWTlFhX1nFmIepe1RNoGq8b'

            UIDS = [
                'UID_D77yyDO0pT7K0f1q2UijDTGnGthF',
            ]
            msg = WxPusher.send_message(content,
                                        uids=UIDS,
                                        token=PUSH_TOKEN)
        except Exception as e:
            print('send_message error--->'+str(e))

if __name__ == '__main__':
    ck = 'pin=jd_694172ad51580;wskey=AAJgfXWSAEBLNQvLpLSYBYcBCqSXPF0LSFJksN9TUW-zjHxTQzDHotSD_LUE5EqkKLhBT3r0b3jCYYm33xg21oLFXWdad7mG;whwswswws=ypBVaXEwFjiJxh/kEB/6O2f6fohXOoCM3D8YNlQLR9tc=;unionwsws={"devicefinger":"eidA852c81205asb09A7r2HGTjCoC1RNl7MXytPQPScu2F6yVo+5IRMfDrQg8oI21UoEA0ZlhW+EgFWItSqxk76gpd5LLB389Tk1jXNw+GmMO1H7tOt5","jmafinger":"ypBVaXEwFjiJxh\/kEB\/6O2f6fohXOoCM3D8YNlQLR9tc="};'
    ck = 'pin=jd_4d36cfba7dab3;wskey=AAJjGfg2AEDbVEKTmVkgEvWx-McNVFq980fU5IHeej0nLaHVNdOtzlTLYBDCEucWGJ4G9teOfEzntfRGd6KQyjXgY3rjDDn1;whwswswws=JD012145b9v1fE5xpOyD1662646298263061cDoZzexYxAp8KLqT9smx6eCUAMi_vgpfvlNGugBkHqboOLvPxFIIgdchS83Af4aCPkH9MZR8ybX3QlO52r5tGF45M9TrieypOzwu3NAoOs0a40rty~w8wI98OE8okFESgoJ3sI8KD1kO1fXEYyQfW7eDyRLBI1VlbD72BRZvaIwvqX8mX245w7Jl7eI9mR2U_2IrtbtCm-NOZyDZr7LWiepMRuTaaO-iRDLr0M_4xyeRgstrh1ombJE27yWpzAQs4PLrFSWhVWGnPf597V0y6FJhG3YaXA;unionwsws={"devicefinger":"eidAea1681212dsbM9nriXryQHq\/kLPLj0nYnTPZ7QyYY2ofy15o7Ohj1DMrIY\/71NnUV3ow\/8dwlD\/hgR5tfjQJNif\/1NbGABbd9A29YETZGl0TuF45","jmafinger":"JD012145b9v1fE5xpOyD1662646298263061cDoZzexYxAp8KLqT9smx6eCUAMi_vgpfvlNGugBkHqboOLvPxFIIgdchS83Af4aCPkH9MZR8ybX3QlO52r5tGF45M9TrieypOzwu3NAoOs0a40rty~w8wI98OE8okFESgoJ3sI8KD1kO1fXEYyQfW7eDyRLBI1VlbD72BRZvaIwvqX8mX245w7Jl7eI9mR2U_2IrtbtCm-NOZyDZr7LWiepMRuTaaO-iRDLr0M_4xyeRgstrh1ombJE27yWpzAQs4PLrFSWhVWGnPf597V0y6FJhG3YaXA"};'
    jdapi = JDSecKillAPI('100012043978', ck)
    print('预约结果--->', jdapi.appoint_sku())
    print('gentoken结果--->', jdapi.get_token_key('100012043978'))
