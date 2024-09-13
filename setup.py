from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()
    
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
    
setup(
    name="validador_docs",
    version="0.0.1",
    author='edmaker89',
    author_email="edmaker@gmail.com",
    description="Description package",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edmaker89/validator_documents_package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.12"
)