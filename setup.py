from os import path
from setuptools import setup, find_packages

project_path = path.abspath(path.dirname(__file__))

with open(
        path.join(project_path, 'requirements.txt'), encoding='utf-8'
) as req_file:
    install_requires = req_file.read()

tests_require = [
    'coverage',
    'response'
]

extras_require = {'tests': tests_require}

setup(
    name='orlylearning',
    version='0.1.0',
    url='https://github.com/Alchemy-Meister/orly-learning',
    author='Alchemy-Meister',
    license='MIT',
    description="Unofficial O'Reilly Learning API for Python 3",
    keywords="O'Reilly, O'Reilly Learning, Safari, Unoficial API",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers'
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require
)
