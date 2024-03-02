from setuptools import setup, find_packages

setup(
    name='alexspawner',
    version='0.0.1',

    packages=find_packages(),
    package_data={
        '': ['templates/*.jinja2']
    },

    author='Alex Egorov',
    author_email='ialex.egorov.mlops@gmail.com',
    description='Description of your library',

    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
