import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

from pretix_emvcoqr import __version__


try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ''


class CustomBuild(build):
    def run(self):
        management.call_command('compilemessages', verbosity=1)
        build.run(self)


cmdclass = {
    'build': CustomBuild
}


setup(
    name='pretix-emvcoqr',
    version=__version__,
    description='Manual payment plugin for pretix with emdeded EMVCo QR Code',
    long_description=long_description,
    url='https://github.com/inwwin/pretix-emvcoqr',
    author='Panawat Wong-klaew',
    author_email='panawat_vista@hotmail.com',
    license='Apache',

    install_requires=['crc16', 'qrcode'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_emvcoqr=pretix_emvcoqr:PretixPluginMeta
""",
)
