import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='qarithmetic',  
    version='0.1',
    author="QArithmetic Development Team",
    author_email="thomaswong@creighton.edu",
    description="Qiskit library for arithmetic and bitwise operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hkhetawat/QArithmetic",
    packages=setuptools.find_packages(),
    install_requires=["qiskit>=0.7.3"],
    py_modules = ['qarithmetic'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
 )


