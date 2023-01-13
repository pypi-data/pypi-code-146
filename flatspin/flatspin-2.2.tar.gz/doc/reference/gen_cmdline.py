from configparser import ConfigParser
cf = ConfigParser()
cf.read('../../setup.cfg')
console_scripts = cf['options.entry_points']['console_scripts']

for line in console_scripts.strip().splitlines():
    print(line)
    prog, mod = line.split('=')
    mod, func = mod.split(':')
    mod = mod.strip()
    prog = prog.strip()
    _, basename = mod.rsplit('.', 1)
    filename = f"cmdline/{basename}.rst"
    print("prog", prog, "mod", mod, "filename", filename)


    doc =  f".. _{prog}:\n\n"
    doc += f".. autoprogram:: {mod}:parser\n"
    doc += f"   :prog: {prog}\n"
    print(filename)
    print(doc)
    with open(filename, 'w') as fp:
        fp.write(doc)
