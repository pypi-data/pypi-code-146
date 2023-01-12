def module_name(pkg_name: str) -> str:
    return pkg_name.replace("-", "_")


def package_name(mod_name: str) -> str:
    return mod_name.replace("_", "-")
