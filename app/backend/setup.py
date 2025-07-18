#!/usr/bin/env python3
"""
Setup script for Prok Professional Networking Backend
"""

import os
import sys
from setuptools import setup, find_packages

# Read requirements from requirements.txt
def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Prok Professional Networking Backend"

setup(
    name="prok-backend",
    version="1.0.0",
    description="Backend API for Prok Professional Networking Platform",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Kumar Shabu",
    author_email="admin@prok.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        'console_scripts': [
            'prok-backend=app:main',
        ],
    },
) 