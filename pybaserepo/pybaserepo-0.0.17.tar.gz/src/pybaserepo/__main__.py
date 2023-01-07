import click


@click.command()
def main():
    click.secho('Hello world', fg='blue')


if __name__ == '__main__':
    main()
