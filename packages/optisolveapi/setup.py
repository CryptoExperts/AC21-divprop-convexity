from distutils.core import setup

setup(
    name='optisolveapi',
    version='1.0.0',
    packages=[
        "optisolveapi",
        "optisolveapi.sat",
        # "optisolveapi.milp",
    ],

    url=None,
    license="MIT",

    author='Aleksei Udovenko',
    author_email="aleksei@affine.group",
    maintainer=None,
    maintainer_email=None,

    description="""Optimization & Solving common API (SAT, MILP, etc.)""",
    long_description=None,
    project_urls={"Source": "https://github.com/CryptoExperts/AC21-DivProp-Convexity"},

    python_requires='>=3.5,<4.0',
    install_requires=[
        # 'python-sat[pblib,aiger]',
        # 'swiglpk',
    ],
)
