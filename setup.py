# setup.py
from setuptools import setup, find_packages

# バージョン情報を読み込む
version = {}
with open("trplots/__version__.py") as fp:
    exec(fp.read(), version)

setup(
    name="trplots",
    version=version["__version__"],
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "seaborn",
    ],
)
