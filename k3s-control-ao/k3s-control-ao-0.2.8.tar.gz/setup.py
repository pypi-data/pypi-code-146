from setuptools import setup, find_packages
version_fn = 'src/k3s_control_ao/version.py'
with open(version_fn, 'r') as f:
    verstr = f.read()
version = verstr.split('=')[1]
version = version.replace("'", "").strip()


setup(
    name="k3s-control-ao",
    version=version,
    author="wangziling100",
    author_email="wangziling100@163.com",
    description="Exposed interface for accessing k3s controller",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)