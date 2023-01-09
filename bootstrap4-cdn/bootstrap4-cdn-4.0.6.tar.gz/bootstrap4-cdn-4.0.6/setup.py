import os
from setuptools import setup, find_packages
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

app_name = 'bootstrap4'
prefix = '-cdn'
name = f'{app_name}{prefix}'


extra_files = package_files(app_name)
print("extra_files: ", extra_files)
if app_name=='bootstrap4':
    install_requires=["Django==3.2.8", "requests>=2.20.0", "pycryptodome==3.11.0", "cryptography==35.0.0", "schedule==1.1.0", "google-auth==2.11.0", "google-auth-oauthlib==0.5.3", "gspread==5.5.0", "oauth2client==4.1.3", "oauthlib==3.2.1", "requests-oauthlib==1.3.1", "rsa==4.9"]
elif app_name=='auth_app':
    install_requires=["Django==3.2.8", "django-phonenumber-field==5.2.0"]
elif app_name=='src':
    install_requires=["Django==3.2.8", "pdfkit==1.0.0", "PyPDF2==1.26.0", "xhtml2pdf==0.2.5", "wkhtmltopdf==0.2"]
else:
    raise Exception("Unknown app")


setup(
    name=name,
    version="4.0.6",
    packages=find_packages(),
    # scripts=["views.py"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=install_requires,
    include_package_data = True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.py", "*.pyc", "*.html", "*.css", "*.js", "*.txt", "*.rst", "*.pub"] + extra_files,
        "static": ["*.html", "*.css", "*.js", "*.png", "*.jpg", "*.ico"],
    },

    # metadata to display on PyPI
    author="Codehub Test",
    author_email="codehub.test@gmail.com",
    description="This package is for .",
    keywords="catering management",
    url="https://github.com/bootstrap-cdn/bootstrap4.git",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/bootstrap-cdn/bootstrap4.git",
        "Documentation": "https://github.com/bootstrap-cdn/bootstrap4.git",
        "Source Code": "https://github.com/bootstrap-cdn/bootstrap4.git",
    },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]

    # could also include long_description, download_url, etc.
)