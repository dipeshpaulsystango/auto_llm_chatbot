from setuptools import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='auto_llm_chatbot',
    version='0.1.0',
    description='A example Python package for LLM chatbot.',
    long_description=long_description,
    url='https://github.com/shuds13/pyexample',
    long_description_content_type="text/markdown",
    author='Dipesh Paul',
    author_email='',
    license='BSD 2-clause',
    project_urls={
        "Bug Tracker": "package issues URL",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=['ollama==0.3.2', 'openai==1.43.0', 'lazyme==0.0.27']
)
