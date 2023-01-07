import setuptools
with open("README.md", "r", encoding="utf-8") as fh: 
    long_description= fh.read()
setuptools.setup( 
      name="scoreMP-pkg-USER-NAME",
      version="0.0.1",
      author="Example Author", 
      author_email="author@example.com", 
      description="A smallexamplepackage", 
      long_description=long_description, long_description_content_type="text/markdown",
       url="https://github.com/pypa/sampleproject", 
       project_urls={ "Bug Tracker": "https://github.com/pypa/sampleproject/issues", })