from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gitchronicle",
    version="1.0.0",
    author="Auto Developer",
    author_email="auto@github.com",
    description="AI-powered Git commit history storytelling and changelog generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/longhao666/GitChronicle",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "gitpython>=3.1.0",
        "click>=8.0.0",
        "rich>=13.0.0",
        "jinja2>=3.0.0",
        "pyyaml>=6.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gitchronicle=gitchronicle.cli:main",
            "gitc=gitchronicle.cli:main",
        ],
    },
)
