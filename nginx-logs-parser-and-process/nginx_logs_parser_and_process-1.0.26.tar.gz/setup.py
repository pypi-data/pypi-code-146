from setuptools import setup, find_packages
import subprocess

git_command_result: subprocess.CompletedProcess = subprocess.run(
    ["git", "describe", "--tags"], capture_output=True, encoding="utf-8"
)
actual_version: str = git_command_result.stdout.strip("\n") or "1.0.1"

setup(
    name="nginx_logs_parser_and_process",
    version=actual_version,
    packages=[
        "nginx_logs_parser_and_process",
        "nginx_logs_parser_and_process.application",
        "nginx_logs_parser_and_process.domain",
        "nginx_logs_parser_and_process.domain.DataProcessor",
        "nginx_logs_parser_and_process.domain.Logs",
        "nginx_logs_parser_and_process.domain.Server",
        "nginx_logs_parser_and_process.domain.Tables",
        "nginx_logs_parser_and_process.infrastructure",
    ],
    url="",
    license="MIT",
    author="Juares Vermelho Diaz",
    author_email="j.vermelho@gmail.com",
    description="Get Logs From Nginx Servers",
    entry_points={
        "console_scripts": [
            "save_remote_nginx_logs = nginx_logs_parser_and_process.cli:process_remote_nginx_logs",
        ]
    },
    install_requires=[
        "click==8.1.3",
        "greenlet==2.0.1; python_version >= '3' and platform_machine == 'aarch64' or (platform_machine == 'ppc64le' or (platform_machine == 'x86_64' or (platform_machine == 'amd64' or (platform_machine == 'AMD64' or (platform_machine == 'win32' or platform_machine == 'WIN32')))))",
        "numpy==1.24.1; python_version < '3.10'",
        "pandas==1.5.2",
        "psycopg2==2.9.5",
        "pydantic==1.10.2",
        "python-dateutil==2.8.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pytz==2022.7",
        "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "sqlalchemy==1.4.45",
        "sysrsync==1.1.0",
        "tabulate==0.9.0",
        "toml==0.10.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "typing-extensions==4.4.0; python_version >= '3.7'",
    ],
)
