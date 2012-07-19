from setuptools import setup

setup(
    name='SnakeGame',
    version='1.0',
    description='The game of Snake, for beginner AI bot writers.',
    author='Peter Ward',
    author_email='peteraward@gmail.com',
    packages=['snakegame'],
    entry_points={
        'console_scripts': [
            'snakegame = snakegame:main',
        ]
    },
)
