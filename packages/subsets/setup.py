import os
from setuptools import setup
from distutils.core import Extension
from pathlib import Path


packages = [
    'subsets',
]

package_data = {
    # '': ['*'],
    'subsets': ['*.hpp', '*.so'],
}

install_requires = [
    'binteger>=0.8.0',
]

entry_points = {
    'console_scripts': [
        'subsets.info = subsets.tools:tool_setinfo',
    ]
}

ext_modules = [
    Extension(
        "subsets._subsets",
        sources=[
            "./subsets/subsets.i",
            "./subsets/BitSet.cpp",
            "./subsets/DenseSet.cpp",
            "./subsets/DenseBox.cpp",
            "./subsets/DenseTernary.cpp",
        ],
        swig_opts=[
            "-c++",
            "-DSWIGWORDSIZE64",  # https://github.com/swig/swig/issues/568
        ],
        include_dirs=[
            "./subsets/",
        ],
        depends=[
            "./subsets/common.hpp",
            "./subsets/hackycpp.hpp",

            "./subsets/Sweep.hpp",
            "./subsets/BitSet.hpp",
            "./subsets/DenseSet.hpp",
            "./subsets/DenseBox.hpp",

            "./subsets/ternary.hpp",
            "./subsets/Sweep3.hpp",
            "./subsets/DenseTernary.hpp",
        ],
        extra_compile_args=["-std=c++2a", "-O3"],
    ),
]


setup(
    name='subsets',
    version='1.1.0',
    packages=packages,

    url=None,
    license="MIT",

    author='Aleksei Udovenko',
    author_email="aleksei@affine.group",
    maintainer=None,
    maintainer_email=None,

    description='Tools for cryptanalysis (binary/box subsets & transforms)',
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
    keywords=[
        "subsets", "binary",
        "multidimensional transforms", "cryptanalysis", "cryptography",
    ],
    project_urls={"Source": "https://github.com/CryptoExperts/AC21-DivProp-Convexity"},

    python_requires='>=3.7,<4.0',
    install_requires=install_requires,

    package_data=package_data,
    entry_points=entry_points,
    ext_modules=ext_modules,
)
