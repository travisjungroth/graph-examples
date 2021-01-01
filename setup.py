import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="graph-examples",
    version="0.0.1",
    author="Travis Jungroth",
    author_email="jungroth@gmail.com",
    description="Examples of graph theory in Pythonic code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/travisjungroth/python-graph-examples",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
