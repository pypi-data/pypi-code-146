import click


@click.group()
def curator():
    """Qbeast Curator commands"""
    pass


@curator.group()
def project():
    """Qbeast Curator Project-related commands"""
    pass

@curator.group()
def snapshot():
    """Qbeast Curator Snapshot-related commands"""
    pass

@curator.group()
def test():
    """Qbeast Curator Test-related commands"""
    pass

@curator.group()
def deployment():
    """Qbeast Curator Deployment-related commands"""
    pass

@curator.group()
def run():
    """Qbeast Curator Run-related commands"""
    pass