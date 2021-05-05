from setuptools import setup

setup(
   name='impfbot',
   version='0.1.0',
   description='A Python scripts which checks periodically for available vaccination appointments',
   author='Henning Storck',
   author_email='mail@henningstorck.com',
   packages=['impfbot'],
   install_requires=['selenium', 'configparser', 'simpleaudio'],
)
