from distutils.core import setup

setup(
    name='justlogs',
    version='1.0.0',
    py_modules=["justlogs"],

    url=None,
    license="MIT",

    author='Aleksei Udovenko',
    author_email="aleksei@affine.group",
    maintainer=None,
    maintainer_email=None,

    description="""Wrapper over coloredlogs with a particular default config""",
    long_description=None,

    python_requires='>=3.5,<4.0',
    install_requires=[
        'coloredlogs',
    ],
)
