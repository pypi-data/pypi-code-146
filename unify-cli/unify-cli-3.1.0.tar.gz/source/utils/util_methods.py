import sys
import click

sys.dont_write_bytecode = True
PYTHONDONTWRITEBYTECODE = 1

def print_stdr(value):
    if value is None:
        return

    text = repr(value)

    try:
        sys.stdout.write(value)
    except UnicodeEncodeError:
        bytes = text.encode(sys.stdout.encoding, 'backslashreplace')
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout.buffer.write(bytes)
        else:
            text = bytes.decode(sys.stdout.encoding, 'strict')
            sys.stdout.write(text)
    sys.stdout.write("\n")


def get_piped_param(ctx, param, value):
    if not value and not click.get_text_stream('stdin').isatty():
        return click.get_text_stream('stdin').read().strip()
    else:
        return value
