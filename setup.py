from setuptools import find_packages, setup

with open('README.md','r', encoding='utf-8-sig') as f:
    readme = f.read()

requirements = [
    "pythainlp>=2.0",
    "requests",
    "xmltodict",
    "pytz"
]

setup(
    name = "pythaiair",
    version = "0.1dev0",
    description = "Thai Air Quality library",
    install_requires = requirements,
    long_description = readme,
    long_description_content_type = "text/markdown",
    author = "Wannaphong Phatthiyaphaibun",
    url = "https://github.com/wannaphong/pythaiair",
    packages = find_packages(),
    python_requires = ">=3.6",
    license = "Apache Software License 2.0",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License"
    ]
)