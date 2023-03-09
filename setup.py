import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="okxpy",
    version="0.0.2",
    author="Enkh-Amar Ganbat",
    description="A pip package for a Python wrapper that provides an interface to the OKX API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["okxpy"],
    package_dir={'':'okxpy'},
    packages=setuptools.find_packages(where="okxpy"),
    package_data={
        'okxpy': ['py.typed'],
    },
    install_requires=[
        "requests",
    ]
)