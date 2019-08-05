import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = '0.0.1'

setuptools.setup(
    name="categorizer",
    version=version,
    author="Higor dos Santos Pinto",
    author_email="higorspinto@gmail.com",
    description="The package reads categories from file and produces a list of frequent categories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/higorspinto/Categorizer",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
)