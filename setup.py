from setuptools import setup, find_packages

setup(
    name='testspace-python',
    version='0.1.5',
    packages=find_packages(include=['testspace', 'testspace.*']),
    url='',
    license="MIT license",
    author="Ivailo Petrov",
    author_email='ivailop@s2technologies.com',
    description="Module for interacting with Testspace Server",
    install_requires=[
        'requests',
    ]
)
