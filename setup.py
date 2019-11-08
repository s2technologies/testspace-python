from setuptools import setup, find_packages

setup(
    name='testspace-python',
    version='',
    packages=find_packages(include=['testspace', 'testspace.*']),
    url='',
    license="MIT license",
    author="Jeffrey Schultz",
    author_email='jeffs@s2technologies.com',
    description="Module for interacting with Testspace Server",
    install_requires=[
        'requests',
    ]
)
