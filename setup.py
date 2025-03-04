from setuptools import setup, find_packages

setup(
    name='dragontg',
    version='0.0.1',
    description='My telegram bot library from 0.',
    url='git@github.com:DragonsCode/dragon-tg.git',
    author='Murodov Dilmurod',
    author_email='dilmurodmurodov978@gmail.com',
    license='MIT',
    packages=find_packages(include=["dragontg", "dragontg.*"]),  # Автоматически находит подмодули
    zip_safe=False
)
