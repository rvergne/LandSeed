import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LandSeed", # Replace with your own username
    version="1.0.0",
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
    entry_points = {
        "console_scripts": [
            "LandSeed=LandSeed.LandSeed.generate"
        ]
    }
)
