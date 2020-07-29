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
