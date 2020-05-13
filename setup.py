from setuptools import setup, find_packages

install_requires = [
    'beautifulsoup4',
    'lxml',
    'requests >= 2.0'
]

tests_require = [
    'coverage',
    'responses',
    'pytest',
    'pytest-cov'
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
        'Intended Audience :: Developers',
        "Operating System :: OS Independent"
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require
)
