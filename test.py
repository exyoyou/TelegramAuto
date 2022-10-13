#!/usr/bin/python3
import base64
import io
import os

import requests
import json

from twocaptcha import TwoCaptcha


class GetImgeCode(object):
    _custom_url_in = "http://2captcha.com/in.php"
    _custom_url_out = "http://2captcha.com/res.php"
    _headers = {
        'Content-Type': 'application/json'
    }
    _key = "49c187f0def8a31cec0ef6a3b8e1c92a"

    def GetCode(self, image):
        imgBase64 = base64.b64encode(image).decode()
        # payload = {
        #     "data": imgBase64,
        #     "key": self._key,
        # }
        # print(imgBase64)
        # resp = requests.post(self._custom_url_in, headers=self._headers, data=json.dumps(payload),)
        # # resp = requests.post(self._custom_url + "?key=" + self._key + "&data=" + imgBase64)
        # print(resp)
        # api_key = os.getenv('APIKEY_2CAPTCHA', 'YOUR_API_KEY')
        solver = TwoCaptcha(self._key)
        # params = {
        #     'key': self._key,
        #     "body": imgBase64,
        # }
        # endpoint = 'http://2captcha.com/in.php'
        # response = requests.post(endpoint, params=params)
        # captcha_id = response.text.split('|')[1]
        solver.


f = open("jmsyzm.jpg", "rb")
img = f.read()
GetImgeCode().GetCode(img)
