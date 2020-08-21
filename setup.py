#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="tap-servicem8",
    version="1.9.0",
    description="Singer.io tap for extracting data from the ServiceM8 API",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_servicem8"],
    install_requires=["singer-python==5.3.3", "requests==2.20.0"],
    extras_require={"dev": ["pylint", "ipdb", "nose",]},
    entry_points="""
          [console_scripts]
          tap-servicem8=tap_servicem8:main
      """,
    packages=["tap_servicem8"],
    package_data={"tap_servicem8": ["tap_servicem8/schemas/*.json"]},
    include_package_data=True,
)
