"""Setup configuration for duckai package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="duckai",
    version="0.1.0",
    author="DuckAI Library Contributors",
    description="Python library for querying DuckDuckGo's AI service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sammatime22/red-hat-server-scripts",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
)
