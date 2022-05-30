from setuptools import setup

setup(
    name='frcpy',
    version='0.2.0-alpha.1',
    description='Library for interacting with The Blue Alliance and Statbotics\'s APIs',
    url='https://github.com/TylerSeiford/frc-py',
    author='Tyler Seiford',
    license='GPLv3',
    packages=['frc_py'],
    install_requires=[
        'tbapy',
        'statbotics'
    ],
    zip_safe=False
)
