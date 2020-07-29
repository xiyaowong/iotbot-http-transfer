# iotbotHTTPTransfer

`转发 iotbot 的 web api，方便远程调用`

## 安装

```shell
pip install git+https://github.com/xiyaowong/iotbot-http-transfer.git@master
```

## 使用

`transfer.py`

```python
from iotbotHTTPTransfer import Transfer

# 定义初始化
app = Transfer(
    iotbot_port=8888,  # iotbot运行的端口号
    iotbot_host='127.0.0.1',  # iotbot运行的ip地址
    timeout=20  # 转发http请求允许的等待时间
)  # 只有三个初始化参数，以上均为默认值
# 三个配置
app.config['key'] = 1234567  # 获取token时需要此参数
app.config['secret_key'] = 'a string that you never guess'  # token加密秘钥，要保证特别复杂
app.config['token_expire'] = 60  # token 有效期，单位为秒, 默认为3天, 最少1分钟以上
# 配置项可以通过设置环境变量设置，优先选用环境变量中的配置
# 环境变量名称均为大写，且在原本字段前加上前缀 TRANSFER_
# 如：TRANSFER_SECRET_KEY = "a secret string."

if __name__ == "__main__":
    # 直接运行
    app.run(
        port=9999,  # 监听的端口
        log=True,  # 日志开关
        host='0.0.0.0'  # 略
    )  # 只有三个参数，以上均为默认值
```

### 使用其他 web 服务器启动

如: `gunicorn -w 4 -b 0.0.0.0:9999 transfer:app`

## 调用 api

1. 因为调用 iotbot 的接口全部需要 token，所以原先的控制面板页肯定不能正常工作，所以就...
2. 获取 token
   例如：`GET http://localhost:9999/genToken?key=1234567` 相应字段对应你的配置
3. 调用 iotbot 的接口除了需要额外加上 token 参数，其他完全一致
   例如：获取当前集群 Cluster 信息
   原：`GET http://host:port/v1/ClusterInfo`
   现：`GET http://host:port/v1/ClusterInfo?token=eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5NjAwNjc5MiwiZXhwIjoxNTk2MDkzMTkyfQ.Im9rLCBpdCcgZnVubnkuIg.MQ-WuAvmTY3f2ZcT_9bTij-mUKEQa38aYnLRWR8_q_FdEz11ug_kyBUgF81qtCU2fDsIZ1TfIhP7ZLMoUkoZFg`

   或者可以设置请求头字段 `Authorization` 为 `token` 值

## 返回码

有时难免程序出问题，所以增加了几个返回码, 如果是程序出错，返回的响应码都是 200 json 格式
如: `200 OK` `{"Ret":1111, "Msg":""}`

| Ret  | Msg                                                                     |
| ---- | ----------------------------------------------------------------------- |
| 1111 | key 错误                                                                |
| 2222 | 无效的 token                                                            |
| 3333 | 请求响应超时, 这里在一些上传大图时会出现，解决办法是将 timeout 参数提高 |
| 4444 | 连接错误, 连接 iotbot 错误，检查 iotbot 是否正常运行，配置是否正确      |
| 5555 | 请求响应失败，这是未知错误                                              |

## LICENSE

MIT
