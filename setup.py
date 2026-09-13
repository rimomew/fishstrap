from setuptools import setup, find_packages

setup(
    name="pyfishstrap",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "requests>=2.28.0",
        "PyQt6>=6.4.0",
    ],
    entry_points={
        "console_scripts": [
            "pyfishstrap=pyfishstrap.main:run",
        ],
    },
)
