from setuptools import setup, find_packages

setup(
    name="hollywoodos",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "textual>=0.45.0",
        "PyYAML>=6.0",
        "typing-extensions>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "hollywoodos=hollywoodos.main:main",
        ],
    },
    python_requires=">=3.11",
)