import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
fh.close()

setuptools.setup(
    name="proofutils",
    version="1.0.2",
    author="ERC Enterprises",
    author_email="heya.discordbot@gmail.com",
    description="ProofUtils, a swift package to generate fake gifting proofs for Discord owners.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ercenterprises/ProofUtils",
    license="LICENSE",
    classifiers=[
         "Development Status :: 4 - Beta",
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
    packages=setuptools.find_packages()
)
