import base64

import requests
from sympy.physics.units import time


class TwoCaptcha(object):
    def __init__(self, _key="49c187f0def8a31cec0ef6a3b8e1c92a"):
        self._key = _key

    _custom_url_in = "http://2captcha.com/in.php"
    _custom_url_res = "http://2captcha.com/res.php"
    _key = "49c187f0def8a31cec0ef6a3b8e1c92a"
    sleep_time = 5
    _req_state = "status"
    _req_request = "request"

    # 获取普通图片验证码
    def get_normal_captcha_code(self, img):
        imgBase64 = base64.b64encode(img).decode()
        req_in = requests.post(self._custom_url_in, data={
            "method": "base64",
            'key': self._key,
            "body": imgBase64,
            'json': 1,
            "lang": "zh",
        })
        in_json = req_in.json()
        if in_json and in_json[self._req_state] and in_json[self._req_state] == 1:
            return self.__get_code_by_id(in_json[self._req_request])
        return in_json[self._req_request]

    # 根据id获取验证的结果 一般只是内部调用
    def __get_code_by_id(self, id):
        req = requests.get(self._custom_url_res, params={
            "action": "get",
            'key': self._key,
            "id": id,
            'json': 1,
        })
        res_json = req.json()
        if res_json and res_json[self._req_state] and res_json[self._req_state] == 1:
            return res_json[self._req_request]
        while 'CAPCHA_NOT_READY' in res_json[self._req_request]:
            time.sleep(self.sleep_time)
            return self.__get_code_by_id(id)
        return res_json[self._req_request]
