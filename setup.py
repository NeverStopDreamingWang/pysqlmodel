"""
@Project:pymysql
@File:setup.py
@Author:函封封
"""

from setuptools import setup, find_packages
setup(
name="SelectModel",
version="0.1.1",
author="HanFengFeng",
author_email="mr_jia_han@qq.com",
description="",
# 项目主页
url="https://gitee.com/wjh-space/py-mysql-model",
# 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
packages=find_packages()
)

# python setup.py sdist bdist_wheel
# twine upload dist/*