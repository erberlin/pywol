from setuptools import setup

setup(
    name="pywol",
    version="0.2.0",
    packages=["pywol"],
    install_requires=["Click"],
    entry_points="""
        [console_scripts]
        pywol=pywol.cli:cli
    """,
)
