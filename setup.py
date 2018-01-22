from setuptools import find_packages
from setuptools import setup

from emissary import VERSION

setup(
    name='emissary',
    version=VERSION,
    description='Proxy service for third party email providers',
    url='https://github.com/zachm/emissary',
    author='Zach Musgrave',
    author_email='ztm@zachm.us',
    license='License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Framework :: Flask',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
    ],

    packages=find_packages(exclude=['tests']),
    install_requires=[],
)
