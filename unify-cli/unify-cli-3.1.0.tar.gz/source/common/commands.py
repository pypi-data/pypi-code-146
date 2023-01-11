import click


class State(object):

    def __init__(self):
        pass


pass_state = click.make_pass_decorator(State, ensure=True)


def cluster_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        state.verbosity = value
        return value

    return click.option(
        '--remote',
        prompt=True,
        hide_input=False,
        required=True,
        confirmation_prompt=False,
        type=click.STRING,
        callback=callback
    )(f)


def org_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        state.debug = value
        return value

    return click.option(
        '--org',
        prompt="Org id",
        hide_input=False,
        default=None,
        required=True,
        type=click.INT,
        callback=callback
    )(f)


def org_cluster_options(f):
    f = cluster_option(f)
    f = org_option(f)
    return f


def org_options(f):
    f = org_option(f)
    return f


def cluster_options(f):
    f = cluster_option(f)
    return f
