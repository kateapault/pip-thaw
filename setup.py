import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="thaw",
    version="0.2",
    author="Kate Raskauskas",
    author_email="kateapault@gmail.com",
    description="Generates report showing where updates will affect your project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kateapault/pip-thaw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
    python_requires='>=3.0',
    keywords="thaw update freeze pip requirements library manage package development project",
)