from setuptools import setup, find_packages

setup(
    name="sortiment",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "kivy>=2.3.0",
        "kivymd @ https://github.com/kivymd/KivyMD/archive/master.zip",
    ],
    author="Patrik Florek",
    author_email="patrikflorek@gmail.com",
    description="A scrollable and drag-n-drop rearrangeable list based on KivyMD.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/patrikflorek/sortiment",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
