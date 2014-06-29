from setuptools import find_packages, setup

setup(
    name='SnakeGame',
    version='1.0',
    description='The game of Snake, for beginner AI bot writers.',
    author='Peter Ward',
    author_email='peteraward@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'six',
    ],
    package_data={
        'snakegame': ['images/*.png'],
    },
    entry_points={
        'console_scripts': [
            'snakegame = snakegame:main',
        ]
    },
)
