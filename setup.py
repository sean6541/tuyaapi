from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tuyaapi',
    version='6.0',
    description='Python interface to Tuya WiFi smart devices.',
    long_description='Python interface to Tuya WiFi smart devices.',
    url='https://tuyaapi.seandev.org',
    author='seandev',
    author_email='seandolson654@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Home Automation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    keywords='home automation',
    packages=["tuyaapi"]
)
