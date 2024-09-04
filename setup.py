from setuptools import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='auto_llm_chatbot',
    version='0.1.0',
    description='A Python package for LLM chatbot with auto RAG Chat History Management.',
    long_description=long_description,
    url='https://github.com/dipeshpaulsystango/auto_llm_chatbot',
    long_description_content_type="text/markdown",
    author='Dipesh Paul',
    author_email='dipesh.paul@systango.com',
    license='MIT License',
    project_urls={
        "GitHub": "https://github.com/dipeshpaulsystango/auto_llm_chatbot",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "auto_llm_chatbot"},
    packages=setuptools.find_packages(where="auto_llm_chatbot"),
    python_requires=">=3.10",
    install_requires=['ollama==0.3.2', 'openai==1.43.0', 'lazyme==0.0.27'],
    include_package_data=True,
)
