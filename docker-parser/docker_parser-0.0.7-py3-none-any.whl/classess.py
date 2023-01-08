from . import dependencies

class Stage:
    def __init__(self, image, commands=[], env={}, args={}, user=None, workdir='/', exposed=[], alias=None):
        self.image = image
        self.alias = alias
        
        self.commands = commands
        self.env = env
        self.args = args
        self.user = user
        self.workdir = workdir
        self.exposed = exposed
    @property
    def name(self):
        return self.alias
    def dumps(self):
        ret = "FROM " + self.image.id + (" as " + self.alias if self.alias else "") +"\n"
        for command in self.commands:
            ret += command.line + '\n'
        return ret

class Docker:
    def __init__(self) -> None:
        self.bases = []
        self.stages = []
        self.lines = None

        self.path = None

        # extensible attributes
        # for extending class with custom data outside of library
        self.extra = {}
    @property
    def exposed(self):
        return self.stages[-1].exposed
    def dumps(self):
        content = "# this file was generated using dockerparser\n"
        for stage in self.stages:
            content +=  '\n' + stage.dumps()
        return content
    def save(self, path=None):
        if not path:
            path = self.path
        with open(path, 'w') as dest:
            dest.write(self.dumps())
    def _get_commands(*cmds):
        """
        Shorcut function to be able to conviniently access specific type of
        command

        @param *args: list of commands to filter (ignores case)
        """
        def wrapper(self, stage=-1):
            if not self.stages or not self.stages[stage].commands:
                return []
            for cmd in self.stages[stage].commands:
                if cmd.command.lower() in cmds:
                    yield cmd
        return wrapper
    run = _get_commands('run')
    copy = _get_commands('copy')
    add = _get_commands('add')
    env = _get_commands('env')
    arg = _get_commands('arg')
    
    def dependencies(self):
        """
        On demand parses dependencies found in code and yields results
        
        @note: currently looks for apt, apt-get, git, wget
        """
        yield from dependencies.get_dependencies(self)