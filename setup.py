from setuptools import setup

setup(
    name="hackwrap",
    version="0.1.0",
    author="Kareem Hashash",
    author_email="kareemhashash2020@gmail.com",
    description="Hack and wrap Python function with decorators.",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kareemhashash/hackwrap",
    py_modules=["hackwrap"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    license="MIT"
)