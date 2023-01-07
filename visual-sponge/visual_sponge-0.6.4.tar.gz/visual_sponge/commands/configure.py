from .. import Configure, ConfigurePath

def CONFIGURE(section, option, value=None):
    if value is None:
        return Configure.get(section, option)
    Configure.set(section, option, value)
    with open(ConfigurePath, "w") as f:
        Configure.write(f)
    return Configure.get(section, option)
