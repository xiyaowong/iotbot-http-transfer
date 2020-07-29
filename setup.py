import io

from setuptools import setup

VERSION = '0.1'


def read_files(files):
    data = []
    for file in files:
        with io.open(file, encoding='utf-8') as f:
            data.append(f.read())
    return "\n".join(data)


long_description = read_files(['README.md'])


setup(
    name="iotbot-http-transfer",
    description="转发iotbot机器人的http接口，便于远程调用",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=VERSION,
    author="wongxy",
    author_email="xiyao.wong@foxmail.com",
    url="https://github.com/xiyaowong/iotbot-http-transfer",
    license='MIT',
    keywords=['iotbot', 'iotbot http', 'iotbot http transfer', 'iotqq', 'iotqq http'],
    packages=['iotbotHTTPTransfer'],
    install_requires=[
        'werkzeug >= 1.0.1', 'itsdangerous >= 1.1.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
