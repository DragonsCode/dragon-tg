from setuptools import setup, find_packages

setup(
    name='dragontg',
    version='0.0.1',
    description='My telegram bot library from 0.',
    url='git@github.com:DragonsCode/dragon-tg.git',
    author='Murodov Dilmurod',
    author_email='dilmurodmurodov978@gmail.com',
    license='MIT',
    packages=find_packages(include=["dragontg", "dragontg.*"]),  # Autodiscover packages
    install_requires=[
        "aiohttp>=3.11.13",  # Library for asynchronous HTTP requests
    ],
    zip_safe=False
)
