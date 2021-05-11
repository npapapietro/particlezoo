from setuptools import find_packages, setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    "liesym>=0.1.2"
]

setup(
    name='particlezoo',
    version='0.0.2',
    description='A particle zoo module',
    install_requires=install_requires,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    test_requires=["pytest"],
    author="Nathan Papapietro <npapapietro95@gmail.com>",
    author_email="npapapietro95@gmail.com",
    url="https://github.com/npapapietro/liesym",
    classifiers=[
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Rust",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
