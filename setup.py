import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="pywol",
    version="1.0.0",
    description="A Wake-on-LAN tool written in Python.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/erberlin/pywol",
    author="Erik R Berlin",
    author_email="erberlin.dev@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pywol"],
    python_requires=">=3.6",
    install_requires=["Click"],
    entry_points="""
        [console_scripts]
        pywol=pywol.cli:cli
    """,
)
