import os
from setuptools import setup
from distutils.core import Extension
from pathlib import Path

# https://stackoverflow.com/questions/29477298/setup-py-run-build-ext-before-anything-else/48942866#48942866
from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    def run(self):
        self.run_command("build_ext")
        return super().run()


try:
    import hackycpp
    HACKYCPP_ROOT = os.path.dirname(hackycpp.__file__)
except ImportError:
    print("Package 'hackycpp' must be instaled before building")
    print("Build dependencies can not be specified yet...")
    print("pip install hackycpp")
    raise

packages = [
    'subsets',
]

package_data = {
    # '': ['*'],
    'subsets': ['*.hpp', '*.so'],
}

install_requires = [
    'hackycpp>=0.1.0',
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
        ],
        swig_opts=[
            "-c++",
            "-DSWIGWORDSIZE64",  # https://github.com/swig/swig/issues/568
            "-I" + HACKYCPP_ROOT,
        ],
        include_dirs=[
            "./subsets/",
            HACKYCPP_ROOT,
        ],
        depends=[
            "./subsets/common.hpp",
            "./subsets/BitSet.hpp",
            "./subsets/DenseSet.hpp",
            "./subsets/DenseBox.hpp",
        ],
        extra_compile_args=["-std=c++2a", "-O3"],
    ),
]


setup(
    cmdclass={'build_py': build_py},  # see above

    name='subsets',
    version='1.0.0',
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
