from setuptools import setup, find_packages
import wxapi

version = wxapi.__version__
author = wxapi.__author__

setup(
    name="wxapi",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    author=author,
    url='https://github.com/cangmean/wxapi',
    install_requires=[
        'requests',
    ]
)