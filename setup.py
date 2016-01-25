from __future__ import unicode_literals

from setuptools import setup, find_packages

from instruction_magic import get_package_version


PACKAGE_NAME = 'bytecode_magic'


setup(name=PACKAGE_NAME,
      version=get_package_version(),
      license='MIT',
      description='Utilities for modifying function bytecode.',
      url='https://github.com/beanbaginc.com/bytecode-magic',
      packages=find_packages(),
      maintainer='Barret Rennie',
      maintainer_email='barret@beanbaginc.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Langauge :: Python :: Implementation :: CPython',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
