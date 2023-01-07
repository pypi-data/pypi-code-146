from setuptools import setup, find_packages

setup(name="visual_sponge",
      version="0.6.4",
      description="A python package to do the visualization for molecular simulations",
      author="Yijie Xia",
      author_email="yijiexia@pku.edu.cn",
      packages=find_packages(),
      package_data = {"":['*.css', '*.js', '*.html', '*.ico', '*.ini', "*.png"]},
      install_requires = ["flask", "Xponge>=1.2.6.12.3", "MDAnalysis", "pyffmpeg"],
      extras_require = {"pyffmpeg":["pyffmpeg"]},
      long_description=open('README.md', encoding="utf-8").read(),
      long_description_content_type="text/markdown",
      entry_points = {
        "console_scripts": ["visual-sponge = visual_sponge.__main__:main"]},
      classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        'Development Status :: 5 - Production/Stable',
        "Operating System :: OS Independent",
        ],
      python_requires='>=3.6',
      )