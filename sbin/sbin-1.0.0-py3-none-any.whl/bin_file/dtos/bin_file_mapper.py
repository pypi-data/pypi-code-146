from pathlib import Path

from bin.bin_file.bin_file_loader import BinFileLoader
from bin.bin_file.dtos.bin_file_dto import BinFileDto
from bin.commands.command import Command


class BinFileMapper:
    @staticmethod
    def to_command(dir_path: Path) -> Command:
        data = BinFileLoader.load(dir_path)
        return BinFileDto.parse_obj_explicitly(data).to_command()

    @staticmethod
    def contains_bin_file(dir_path: Path) -> bool:
        return BinFileLoader.find_any_bin_file(dir_path) is not None

    @staticmethod
    def example_file_content() -> str:
        return """name: my project
description: is pretty cool

env:
  APP_ENV: dev
  DB_URL: postgresql://mydb.local:5432/database
  DB_PASSWORD: imsupersecure123

requirements:
  - name: Docker
    met_if: echo docker --version
    help: Download docker @ https://docker.com

venv:
  create: echo create venv
  exists: echo test -e venv
  activate: echo activate venv
  remove: echo rm venv

up:
  - echo always run
  - name: docker-compose
    up: echo docker-compose up -d
    up_unless: echo docker up unless
    down: echo docker-compose down
    down_unless: echo docker down unless

commands:
  server: echo run server
  test:
    run: echo run tests
    alias: t
    env:
      APP_ENV: test
  lint:
    run: echo lint all
    aliases:
      - format
      - style
      - check
    subcommands:
      frontend: echo frontend lint
      backend: echo backend lint
"""
