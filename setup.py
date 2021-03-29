
from setuptools import setup, find_packages

setup(
    name="block_server",
    packages=find_packages('src'),
    package_dir={'': 'src'}
)
