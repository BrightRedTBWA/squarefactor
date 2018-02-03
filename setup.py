#!/usr/bin/env python
from distutils.core import setup


VERSION = '1.0.0'

README_FILE = open('README')
try:
    long_description = README_FILE.read()
finally:
    README_FILE.close()

setup(
    name='squarefactor',
    version=VERSION,
    url='https://github.com/BrightRedTBWA/squarefactor',
    download_url='https://github.com/BrightRedTBWA/squarefactor',
    description='squarefactor django app base. **DEPRECATED**',
    long_description=long_description,
    author='',
    platforms=['any'],
    packages=[
        'squarefactor',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
