import os

import pkg_resources
from setuptools import setup, find_packages

setup(
    name="gector",
    py_modules=["gector"],
    version="1.0",
    description="",
    readme="README.md",
    python_requires=">=3.7",
    author="",
    url="https://github.com/Tequip/gector",
    license="MIT",
    packages=find_packages('gector', include=['gector.*']),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    include_package_data=True,
)
