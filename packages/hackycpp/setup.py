#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='hackycpp',
    version='1.0.0',
    packages=["hackycpp"],

    author='Aleksei Udovenko',
    author_email="aleksei@affine.group",
    maintainer=None,
    maintainer_email=None,

    description="""HackyCPP (loop macros and etc. for surviving C++)""",
    long_description=None,

    package_data={'hackycpp': ['*.h', '*.so']},

    url=None,
    license="MIT",

    python_requires='>=3.4,<4.0',
)
