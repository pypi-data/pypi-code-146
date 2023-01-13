from pkg_resources import resource_filename

with open(resource_filename(__name__.rsplit('.', 1)[0], 'VERSION')) as vf:
    version_str = vf.read().strip()
