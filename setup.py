import setuptools
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for dir in directories:
            paths.append(os.path.join(path.replace('LandSeed/', ''),dir, "*"))
    return paths

extra_files = package_files('LandSeed/data')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LandSeed",
    version="1.0.11",
    author="Bastien Zigmann",
    author_email="bastien@zigmann.org",
    description="Procedural terrain shader generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sauww/LandSeed",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.0',
    install_requires=[
        'numpy>=1.18.1',
        'glfw>=1.11.1',
        'PyOpenGL>=3.1.5'
    ],
    entry_points = {
        "console_scripts": [
            "LandSeed=LandSeed.LandSeed:generate",
            "LandSeed_newinput=LandSeed.LandSeed:newInputFile"
        ]
    },
    include_package_data=True,
    package_data={'':extra_files+["input/demo*.frag"],},
)

# TODO :
#  - check classifier
