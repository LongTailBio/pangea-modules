"""Macro module for Pangea Modules.

Based on: https://blog.shazam.com/python-microlibs-5be9461ad979
"""


import os
import pip
from six import iteritems
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


PACKAGE_NAME = 'pangea_modules'


SOURCES = {
  'pangea_modules.base': 'modules/base',
  'pangea_modules.kraken': 'modules/kraken',
}


def install_microlibs(sources, develop=False):
    """ Use pip to install all microlibraries.  """
    print('Installing all microlibs in {} mode'.format(
              'development' if develop else 'normal'))
    working_dir = os.getcwd()
    for name, path in iteritems(sources):
        try:
            os.chdir(os.path.join(working_dir, path.root_dir))
            if develop:
                pip.main(['install', '-e', '.'])
            else:
                pip.main(['install', '.'])
        except Exception as e:
            print('Oops, something went wrong installing', name)
            print(e)
        finally:
            os.chdir(working_dir)


class DevelopCmd(develop):
    """ Add custom steps for the develop command """
    def run(self):
        install_microlibs(SOURCES, develop=True)
        develop.run(self)


class InstallCmd(install):
    """ Add custom steps for the install command """
    def run(self):
        install_microlibs(SOURCES, develop=False)
        install.run(self)


setup(
    name=PACKAGE_NAME,
    version='0.1.2',
    author='Longtail Biotech',
    author_email='dev@longtailbio.com',
    description='Core modules for use with Longtail Biotech\'s Pangea platform.',
    license='Restricted',
    classifiers=[
        'Private :: Do Not Upload to pypi server',
    ],
    install_requires=[
        'future',
        'six',
    ],
    cmdclass={
        'install': InstallCmd,
        'develop': DevelopCmd,
    },
)
