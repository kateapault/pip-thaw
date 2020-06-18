import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="pip-thaw",
    version="0.0.1",
    author="Kate Raskauskas",
    author_email="kateapault@gmail.com",
    description="Update CLI utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kateapault/pip-thaw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)