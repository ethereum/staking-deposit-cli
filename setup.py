from setuptools import find_packages, setup
from staking_deposit.version import __version__

"""
THIS IS A STUB FOR RUNNING THE APP
"""

setup(
    name="staking_deposit",
    version=__version__,
    py_modules=["staking_deposit"],
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires=">=3.8,<4",
)
