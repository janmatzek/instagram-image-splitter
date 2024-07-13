from setuptools import setup, find_packages

setup(
    name="insta-splitter",
    version="0.1",
    packages=find_packages(),
    py_modules=["splitter"],
    entry_points={
        'console_scripts': [
            'splitter = splitter:main',
        ],
    },
    install_requires=[
        "pillow",
    ],
)