"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""


def filterModules(name_:str, file_: str) -> [str]:
    import os.path

    for module in os.listdir(os.path.dirname(file_)):
        modName, modExt = module.rsplit('.', 1) if '.' in module else [module, '']
        if modExt not in ('py', 'pyc'):
            continue

        if modName == '__init__':
            continue

        if modName.endswith("Test"):
            continue

        yield '%s.%s' % (name_, module.rsplit('.', 1)[0])
