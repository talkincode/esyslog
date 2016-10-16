#!/usr/bin/python

from setuptools import setup, find_packages
import esyslog

version = esyslog.__version__

install_requires = [
    'Twisted>=15.0.0',
    'pytz'
]
install_requires_empty = []

package_data={
}


setup(name='esyslog',
      version=version,
      author='jamiesun',
      author_email='jamiesun.net@gmail.com',
      url='https://github.com/talkincode/esyslog',
      license='Apache License',
      description='syslog tools',
      long_description=open('README.md').read(),
      classifiers=[
       'Development Status :: 6 - Mature',
       'Intended Audience :: Developers',
       'Programming Language :: Python :: 2.6',
       'Programming Language :: Python :: 2.7',
       'Topic :: Software Development :: Libraries :: Python Modules',
       ],
      packages=find_packages(),
      package_data=package_data,
      keywords=['syslog', 'elk','elasticsearch'],
      zip_safe=True,
      include_package_data=True,
      eager_resources=['esyslog'],
      install_requires=install_requires,
      entry_points={
          'console_scripts': [
              'esyslogd = esyslog.syslog_server:main'
          ]
      }
)