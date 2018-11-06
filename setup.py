from setuptools import setup, find_packages

setup(
    name='Json parser',
    version='0.0.1',
    author='Piotr Dankowski',
    description='working with jsons example',
    package_dir={'json_parser': 'json_parser'},
    packages=find_packages(),
    install_requires=[
        'autopep8',
        'requests'
    ],
    entry_points={
        'console_scripts': ['json_parser=json_parser.entrypoint:main'],
    },
)