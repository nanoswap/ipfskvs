"""Setup."""
from setuptools import find_packages, setup

from ipfskvs import __version__


def load_long_description(filename: str) -> str:
    """Convert README.md to a string."""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="ipfskvs",
    version=__version__,
    author="Nathaniel Schultz",
    author_email="nate@nanoswap.finance",
    description="IPFS Key Value Store",
    long_description=load_long_description("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/nanoswap/ipfskvs",
    project_urls={
        "Bug Tracker": "https://github.com/nanoswap/ipfskvs/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)"
    ],
    package_dir={'ipfskvs': "ipfskvs"},
    packages=find_packages(exclude=['tests', 'tests.*']),
    python_requires=">=3.11"
)
