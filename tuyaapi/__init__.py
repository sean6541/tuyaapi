import requests
import time
import hashlib
import json
import socket

ACCESS_ID = 'nvusfxamhprcxgcnpd9n'
ACCESS_KEY = '9dxjmakk5ar4qwwfpjdyneafcvq7hnmf'

DEV_IP = '192.168.4.1'

class TuyaAPI(object):
    def __init__(self, USER_EMAIL, USER_PASSWD):
        self.USER_EMAIL = USER_EMAIL
        self.USER_PASSWD = USER_PASSWD
        self.sid = None
        self.login()

    def requestapi(self, cmd, dataa, needsid = False):
        accessid = ACCESS_ID
        accesskey = ACCESS_KEY
        data = json.dumps(dataa, separators=(',', ':'))
        timee = str(int(time.time()))
        h1 = hashlib.md5()
        h1.update(data.encode())
        datam = h1.hexdigest()
        datamd = datam[8:16] + datam[0:8] + datam[24:32] + datam[16:24]
        if needsid == True:
            signun = 'a=' + cmd + '||clientId=' + accessid + '||lang=en||os=Linux||postData=' + datamd + '||sid=' + self.sid + '||time=' + timee + '||v=1.0||' + accesskey
            h2 = hashlib.md5()
            h2.update(signun.encode())
            sign = h2.hexdigest()
            url = 'https://a1.tuyaus.com/api.json?a=' + cmd + '&clientId=' + accessid + '&lang=en&os=Linux&sid=' + self.sid + '&time=' + timee + '&v=1.0&sign=' + sign
        else:
            signun = 'a=' + cmd + '||clientId=' + accessid + '||lang=en||os=Linux||postData=' + datamd + '||time=' + timee + '||v=1.0||' + accesskey
            h2 = hashlib.md5()
            h2.update(signun.encode())
            sign = h2.hexdigest()
            url = 'https://a1.tuyaus.com/api.json?a=' + cmd + '&clientId=' + accessid + '&lang=en&os=Linux&time=' + timee + '&v=1.0&sign=' + sign
        respr = requests.post(url, data={'postData':data})
        resp = json.loads(respr.text)
        return resp

    def requestdev(self, data):
        dataunh = json.dumps(data, separators=(',', ':'))
        datatoenc = dataunh.encode('latin1')
        l1 = chr(len(datatoenc) + 8).encode('latin1')
        prefix = '\x00\x00\x55\xaa\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'.encode('latin1')
        suffix = '\x95\x60\xcb\x82\x00\x00\xaa\x55'.encode('latin1')
        finaldata = prefix + l1 + datatoenc + suffix
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('0.0.0.0', 6670))
        s.sendto(finaldata, (DEV_IP, 6669))
        s.close()
        return

    def login(self):
        cmd = 'tuya.m.user.email.password.login'
        data = {
            'countryCode': 1,
            'email': self.USER_EMAIL,
            'passwd': self.USER_PASSWD
        }
        resp = self.requestapi(cmd, data)
        if resp['success'] == False:
            cmd2 = 'tuya.m.user.email.register'
            data2 = {
                'countryCode': 1,
                'email': self.USER_EMAIL,
                'passwd': self.USER_PASSWD
            }
            resp2 = self.requestapi(cmd2, data2)
            self.sid = resp2['result']['sid']
        else:
            self.sid = resp['result']['sid']
        return

    def logout(self):
        cmd = 'tuya.m.user.loginout'
        data = {
            'timeZone': '+00:00'
        }
        self.requestapi(cmd, data, True)
        return

    def gentok(self):
        cmd = 'tuya.m.device.token.create'
        data = {
            'timeZone': '+00:00'
        }
        resp = self.requestapi(cmd, data, True)
        res = {
            'token': resp['result']['token'],
            'secret': resp['result']['secret']
        }
        return res

    def setupdev(self, ssid, passwd, token, secret):
        data = {
            'passwd': passwd,
            'ssid': ssid,
            'token': 'AZ' + token + secret
        }
        self.requestdev(data)
        return

    def ldevbytok(self, token):
        cmd = 'tuya.m.device.list.token'
        data = {
            'token': token
        }
        resp = self.requestapi(cmd, data, True)
        devid = resp['result'][0]['id']
        return devid

    def ldevbyuser(self):
        cmd = 'tuya.m.device.list'
        data = {}
        resp = self.requestapi(cmd, data, True)
        devs = []
        for dev in resp['result']['devices']:
            sws = len(dev['dps']) - 1
            devs.append({'devid': dev['devId'], 'sws': sws, 'name': dev['name']})
        return devs

    def getsws(self, dev):
        cmd = 'tuya.m.device.dp.get'
        data = {
            'devId': dev
        }
        resp = self.requestapi(cmd, data, True)
        dps = resp['result']
        sws = len(dps) - 1
        return sws

    def getdevname(self, dev):
        cmd = 'tuya.m.device.get'
        data = {
            'devId': dev
        }
        resp = self.requestapi(cmd, data, True)
        name = resp['result']['name']
        return name

    def setdevname(self, dev, name):
        cmd = 'tuya.m.device.name.update'
        data = {
            'devId': dev,
            'name': name
        }
        self.requestapi(cmd, data, True)
        return

    def getdps(self, dev):
        cmd = 'tuya.m.device.dp.get'
        data = {
            'devId': dev
        }
        resp = self.requestapi(cmd, data, True)
        dps = resp['result']
        dpss = {}
        i = 1
        for key, value in dps.items():
            if i != len(dps):
                dpss[key] = value
                i = i + 1
        return dpss

    def setdps(self, dev, dps):
        cmd = 'tuya.m.device.dp.publish'
        data = {
            'devId': dev,
            'dps': dps
        }
        self.requestapi(cmd, data, True)
        return

class TuyaDevice(object):
    def __init__(self, tapi, dev):
        self.tapi = tapi
        self.dev = dev

    def getsws(self):
        sws = self.tapi.getsws(self.dev)
        return sws

    def getname(self):
        name = self.tapi.getdevname(self.dev)
        return name

    def setname(self, name):
        self.tapi.setdevname(self.dev, name)
        return

    def getstate(self, swid = 1):
        dps = self.tapi.getdps(self.dev)
        state = dps[str(swid)]
        return state

    def setstate(self, state, swid = 1):
        dps = {str(swid): state}
        self.tapi.setdps(self.dev, dps)
        return
