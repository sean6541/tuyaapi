import requests
import time
import hashlib
import json
import socket

ACCESS_ID = 'nvusfxamhprcxgcnpd9n'
ACCESS_KEY = '9dxjmakk5ar4qwwfpjdyneafcvq7hnmf'

class TuyaAPI(object):
    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd
        self.sid = None
        cmd = 'tuya.m.user.email.password.login'
        data = {
            'countryCode': 1,
            'email': self.email,
            'passwd': self.passwd
        }
        resp = self.requestapi(cmd, data)
        if resp == False:
            cmd2 = 'tuya.m.user.email.register'
            data2 = {
                'countryCode': 1,
                'email': self.email,
                'passwd': self.passwd
            }
            resp2 = self.requestapi(cmd2, data2)
            self.sid = resp2['sid']
        else:
            self.sid = resp['sid']

    def requestapi(self, cmd, dataa):
        data = json.dumps(dataa, separators=(',', ':'))
        timee = str(int(time.time()))
        h1 = hashlib.md5()
        h1.update(data.encode())
        datam = h1.hexdigest()
        datamd = datam[8:16] + datam[0:8] + datam[24:32] + datam[16:24]
        if self.sid != None:
            signun = 'a=' + cmd + '||clientId=' + ACCESS_ID + '||lang=en||os=Linux||postData=' + datamd + '||sid=' + self.sid + '||time=' + timee + '||v=1.0||' + ACCESS_KEY
            h2 = hashlib.md5()
            h2.update(signun.encode())
            sign = h2.hexdigest()
            url = 'https://a1.tuyaus.com/api.json?a=' + cmd + '&clientId=' + ACCESS_ID + '&lang=en&os=Linux&sid=' + self.sid + '&time=' + timee + '&v=1.0&sign=' + sign
        else:
            signun = 'a=' + cmd + '||clientId=' + ACCESS_ID + '||lang=en||os=Linux||postData=' + datamd + '||time=' + timee + '||v=1.0||' + ACCESS_KEY
            h2 = hashlib.md5()
            h2.update(signun.encode())
            sign = h2.hexdigest()
            url = 'https://a1.tuyaus.com/api.json?a=' + cmd + '&clientId=' + ACCESS_ID + '&lang=en&os=Linux&time=' + timee + '&v=1.0&sign=' + sign
        respr = requests.post(url, data={'postData':data})
        resp = json.loads(respr.text)
        if resp['success'] == True:
            respd = resp['result']
        else:
            respd = False
        return respd

    def ldevbyuser(self):
        cmd = 'tuya.m.device.list'
        data = {}
        resp = self.requestapi(cmd, data)
        devs = resp['devices']
        return devs

    def getdevname(self, dev):
        cmd = 'tuya.m.device.get'
        data = {
            'devId': dev
        }
        resp = self.requestapi(cmd, data)
        name = resp['name']
        return name

    def setdevname(self, dev, name):
        cmd = 'tuya.m.device.name.update'
        data = {
            'devId': dev,
            'name': name
        }
        self.requestapi(cmd, data)
        return

class DevSetup(object):
    def __init__(self, tapi, ssid, passw):
        self.tapi = tapi
        self.ssid = ssid
        self.passw = passw
        self.token = None
        self.secret = None
        cmd = 'tuya.m.device.token.create'
        data = {
            'timeZone': '+00:00'
        }
        resp = self.tapi.requestapi(cmd, data)
        self.token = resp['token']
        self.secret = resp['secret']

    def setupdev(self):
        data = {
            'passwd': self.passw,
            'ssid': self.ssid,
            'token': 'AZ' + self.token + self.secret
        }
        dataunh = json.dumps(data, separators=(',', ':'))
        datatoenc = dataunh.encode('latin1')
        l1 = chr(len(datatoenc) + 8).encode('latin1')
        prefix = '\x00\x00\x55\xaa\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'.encode('latin1')
        suffix = '\x95\x60\xcb\x82\x00\x00\xaa\x55'.encode('latin1')
        finaldata = prefix + l1 + datatoenc + suffix
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('0.0.0.0', 6670))
        s.sendto(finaldata, ('192.168.1.4', 6669))
        s.close()
        return

    def ldevbytok(self):
        cmd = 'tuya.m.device.list.token'
        data = {
            'token': self.token
        }
        resp = self.tapi.requestapi(cmd, data)
        devid = resp[0]['id']
        return devid

class TuyaSwitch(object):
    def __init__(self, tapi, dev):
        self.tapi = tapi
        self.dev = dev

    def getsws(self):
        cmd = 'tuya.m.device.dp.get'
        data = {
            'devId': self.dev
        }
        resp = self.tapi.requestapi(cmd, data)
        sws = len(resp) - 1
        return sws

    def getname(self):
        name = self.tapi.getdevname(self.dev)
        return name

    def setname(self, name):
        self.tapi.setdevname(self.dev, name)
        return

    def getstate(self, swid = 1):
        cmd = 'tuya.m.device.dp.get'
        data = {
            'devId': self.dev
        }
        resp = self.tapi.requestapi(cmd, data)
        return resp[str(swid)]

    def setstate(self, state, swid = 1):
        cmd = 'tuya.m.device.dp.publish'
        data = {
            'devId': self.dev,
            'dps': {
                str(swid): state
            }
        }
        self.tapi.requestapi(cmd, data)
        return
