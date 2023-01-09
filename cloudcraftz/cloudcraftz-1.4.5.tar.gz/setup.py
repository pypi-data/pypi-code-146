from setuptools import setup, find_packages

try:
    REQUIRES = list()
    f = open("requirements.txt", "rb")
    for line in f.read().decode("utf-8").split("\n"):
        line = line.strip()
        if "#" in line:
            line = line[: line.find("#")].strip()
        if line:
            REQUIRES.append(line)
except FileNotFoundError:
    print("'requirements.txt' not found!")
    REQUIRES = list()

url_path = 'www.cloudcraftz.com'

setup(name='cloudcraftz',
      version = '1.4.5',
      license = f"Cloudcraftz Solutions Pvt. Ltd. - {url_path}",
      author = "Neelakash Chatterjee",
      packages = find_packages(),
      install_requires = REQUIRES,
      description = "Cloudcraftz: A Library for Financial Data Analysis and Pre-Processing.",
      )
