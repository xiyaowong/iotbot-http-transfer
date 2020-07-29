"""Author: wongxy

github.com/xiyaowong/iotbot-http-transfer

>>> from iotbotHTTPTransfer import Transfer

>>> transfer = Transfer()
>>> transfer.config['key'] = 1234567
>>> transfer.config['secret_key'] = 'a string that you never guess'
>>> transfer.config['token_expire'] = 60

>>> app.run(9999)
"""
import json
import logging
import os

import itsdangerous
import requests
from requests.api import head
from werkzeug import Request
from werkzeug import Response
from werkzeug.http import HTTP_STATUS_CODES


class InvalidSettingError(Exception):
    """无效数据"""


class Transfer:
    """iotbot http请求中转
    :param iotbot_port: iotbot运行的端口号
    :param iotbot_host: iotbot运行的ip地址
    :param timeout: 转发http请求允许的等待时间
    """

    def __init__(self,
                 iotbot_port=8888,
                 iotbot_host='127.0.0.1',
                 timeout=20) -> None:
        self.iotbot_host = iotbot_host
        self.iotbot_port = iotbot_port
        self.timeout = timeout
        self.config = dict()
        self.logger = logging.getLogger('iotbotHTTPTransfer')

    def _initial_key(self):
        key = (os.getenv('TRANSFER_KEY')
               or self.config.get('KEY')
               or self.config.get('key'))
        if key is None or len(str(key)) < 6:
            raise InvalidSettingError('必须设置 key , 并且长度不能小于6')
        self.key = str(key)  # key 统一为str

    def __call__(self, environ, start_response):
        # 放这里好别扭，但是不知道该放哪了
        self._initial_key()
        self._initial_serializer()
        return self._application(environ, start_response)

    def run(self, port=7788, log=True, host='0.0.0.0'):
        """
        :param port: 开启web服务的端口
        :param log: 日志开关
        :param host: host
        """
        if not log:
            logging.disable()
        from werkzeug import run_simple
        run_simple(host, port, self)

    def _application(self, environ, start_response):
        request = Request(environ)
        self.logger.info(request.full_path)

        status_code = 200
        headers = {'Content-Type': 'application/json'}
        content = ''

        if request.path == '/':  # 接管主页，因为所有请求需要token，主页转发不能正常工作
            headers = {'Content-Type': 'text/html'}
            content = '<h1><a href="https://github.com/xiyaoWong/iotbot-http-transfer">iotbot http tranfer</a><h1>'
        elif request.path.strip('/') == 'favicon.ico':
            status_code = 301
            del headers['Content-Type']
            headers['location'] = 'https://cdn.jsdelivr.net/gh/xiyaowong/FileHost/transfer.png'
        elif request.path.strip('/') == 'genToken':  # 处理token生成请求
            key = request.args.get('key')
            if key == self.key:
                token = self._genarate_token('ok, it\' funny.')
                content = json.dumps({'token': token})
            else:
                content = '{"Ret":1111, "Msg":"key错误"}'
        else:  # 处理其他请求
            # 鉴权
            token = request.args.get('token') or request.headers.get('Authorization')
            if not self._check_token(token):  # 大胆，狗贼
                content = '{"Ret":2222, "Msg":"无效的token"}'
            else:
                try:
                    resp = requests.request(
                        request.method,
                        '{}{}?{}'.format(
                            'http://{}:{}'.format(self.iotbot_host, self.iotbot_port),
                            request.path,
                            request.query_string.decode()),
                        headers=request.headers,
                        data=request.data,
                        timeout=self.timeout
                    )
                except requests.Timeout as e:
                    self.logger.warning(e)
                    content = '{"Ret":3333, "Msg":"请求响应超时"}'
                except requests.ConnectionError as e:
                    self.logger.exception(e)
                    content = '{"Ret":4444, "Msg":"连接错误"}'
                except Exception as e:
                    self.logger.exception(e)
                    content = '{"Ret":5555, "Msg":"请求响应失败"}'
                else:
                    content = resp.content
                    status_code = resp.status_code
                    headers = resp.headers

        response = Response(content)
        response.status = HTTP_STATUS_CODES[status_code]
        response.status_code = status_code
        for header_name, header_value in headers.items():
            response.headers[header_name] = header_value
        return response(environ, start_response)

    def _initial_serializer(self):
        secret_key = (os.getenv('TRANSFER_SECRET_KEY')
                      or self.config.get('SECRET_KEY')
                      or self.config.get('secret_key'))
        expire = (os.getenv('TRANSFER_TOKEN_EXPIRE')
                  or self.config.get('TOKEN_EXPIRE')
                  or self.config.get('token_expire'))

        if secret_key is None or len(str(secret_key)) < 6:
            raise InvalidSettingError('必须设置 secret_key , 并且长度不能小于6')
        secret_key = str(secret_key)  # secret_key 统一为str

        if expire is not None:
            if not str(expire).isdigit():
                raise InvalidSettingError('过期时间必须为数字')
            expire = int(expire)
            if expire < 1 * 60:
                raise InvalidSettingError('过期时间至少为 1 分钟')
        else:
            expire = 1 * 24 * 60 * 60  # otken有效时间默认为一天
        self.serializer = itsdangerous.TimedJSONWebSignatureSerializer(secret_key, expires_in=expire)

    def _genarate_token(self, data) -> str:
        return self.serializer.dumps(data).decode()

    def _check_token(self, token) -> bool:
        try:
            self.serializer.loads(token)
        except Exception:
            return False
        return True
