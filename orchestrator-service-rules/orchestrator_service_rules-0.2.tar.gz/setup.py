from setuptools import setup


setup(
    name="orchestrator_service_rules",
    version="0.2",
    description="orchestrator for code execution through a rule",
    author="Daniel Garcia Uscanga",
    author_email="daniel.garcia@tangelolatam.com",    
    packages=[
        'orchestrator_service_rules'],
    scripts=[],
    install_requires=[
        "PyYAML==6.0",
        "python-decouple==3.6"
    ]    
)
