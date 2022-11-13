#!/usr/bin/env python

from setuptools import setup

setup(
    name="tap-servicem8",
    version="1.0.0",
    description="Singer.io tap for extracting data from the ServiceM8 API",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_servicem8"],
    install_requires=["pipelinewise-singer-python==1.*", "requests==2.25.1"],
    extras_require={
        "dev": [
            "pylint",
            "ipdb",
            "nose",
        ]
    },
    entry_points="""
          [console_scripts]
          tap-servicem8=tap_servicem8:main
      """,
    packages=["tap_servicem8"],
    package_data={"tap_servicem8": ["tap_servicem8/schemas/*.json"]},
    include_package_data=True,
)
