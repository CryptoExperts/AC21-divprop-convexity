import os
from setuptools import setup
from distutils.core import Extension

# https://stackoverflow.com/questions/29477298/setup-py-run-build-ext-before-anything-else/48942866#48942866
from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    def run(self):
        self.run_command("build_ext")
        return super().run()


try:
    import hackycpp
    HACKYCPP_ROOT = os.path.dirname(hackycpp.__file__)
    HACKYCPP_HPP = os.path.join(HACKYCPP_ROOT, "hackycpp.h")
except ImportError:
    print("Package 'hackycpp' must be instaled before building")
    print("Build dependencies can not be specified yet...")
    print("pip install hackycpp")
    raise

try:
    import subsets
    SUBSETS_ROOT = os.path.dirname(subsets.__file__)
    SUBSETS_SO = subsets._subsets.__file__
except ImportError:
    print("Package 'subsets' must be instaled before building")
    print("Build dependencies can not be specified yet...")
    print("pip install subsets")
    raise

package_dir = {'': 'src'}

packages = [
    'divprop',
]

package_data = {
    # '': ['*'],
    'divprop': ['*.so', '*.hpp'],
}

install_requires = [
    'binteger>=0.8.0',
    'coloredlogs>=15.0',
    'tqdm>=4.58.0',

    'subsets>=0.1.0',
    'justlogs>=0.1.0',
    'hackycpp>=0.1.0',
    # 'optisolveapi>=0.1.0',
]

entry_points = {
    'console_scripts': [
        'divprop.sbox2ddt = divprop.tools:tool_sbox2ddt',
        'divprop.sbox2ptt = divprop.tools:tool_sbox2ptt',
        'divprop.sbox2divcore = divprop.tools:tool_sbox2divcore',
        'divprop.divcore2bounds = divprop.tools:tool_divcore2bounds',

        'divprop.random_sbox_benchmark = '
        + 'divprop.tool_random_sbox_benchmark:tool_RandomSboxBenchmark',
    ]
}

setup(
    cmdclass={'build_py': build_py},  # see above

    name='divprop',
    version='0.2.1',
    packages=packages,

    url=None,
    license="MIT",

    author='Aleksei Udovenko',
    author_email="aleksei@affine.group",
    maintainer=None,
    maintainer_email=None,

    description='Tools for cryptanalysis (division property)',
    long_description=None,
    project_urls={"Source": "https://github.com/CryptoExperts/AC21-DivProp-Convexity"},

    python_requires='>=3.7,<4.0',
    install_requires=install_requires,

    package_dir=package_dir,
    package_data=package_data,
    entry_points=entry_points,
    ext_modules=[
        Extension(
            "divprop._lib",
            include_dirs=[
                "./src/",
                "./src/sbox/",
                "./src/divprop/divprop/",
                HACKYCPP_ROOT,
                SUBSETS_ROOT,
            ],
            depends=[
                "./src/divprop/divprop/DivCore.hpp",
                "./src/sbox/Sbox.hpp",
                SUBSETS_SO,
                HACKYCPP_HPP,
            ],
            sources=[
                "./src/divprop/lib.i",
                "./src/sbox/Sbox.cpp",
            ],
            swig_opts=[
                "-c++",
                "-DSWIGWORDSIZE64",  # https://github.com/swig/swig/issues/568
                "-I" + HACKYCPP_ROOT,
                "-I" + SUBSETS_ROOT,
            ],
            extra_compile_args=["-std=c++2a", "-O3", "-fopenmp"],
            extra_link_args=["-fopenmp", SUBSETS_SO],
        ),
    ]
)
