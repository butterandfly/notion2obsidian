import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="notion2obsidian",
    version="0.1.1",
    description="Convert Notion md files to Obsidian md files.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/butterandfly/notion2obsidian",
    author="butterandfly",
    author_email="zero.hero.lin@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["notion2obsidian"],
    include_package_data=True,
    install_requires=["rich"],
    entry_points={
        "console_scripts": [
            "notion2obsidian=notion2obsidian.__main__:main",
        ]
    },
)

