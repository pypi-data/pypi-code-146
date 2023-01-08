import re
import os
import bashlex
from .classess import Docker, Stage

class ParsingError(Exception):
    pass

class UnsupportedError(Exception):
    pass

def bashlex_iter(part):
    if hasattr(part, 'word'):
        yield part.word
    elif hasattr(part, 'op'):
        yield part.op
    elif hasattr(part, 'kind') and part.kind == "redirect":
        yield part.type
        yield from bashlex_iter(part.input)
        yield from bashlex_iter(part.output)
    elif hasattr(part, 'parts'):
        for sub in part.parts:
            yield from bashlex_iter(sub)

def bashlex_commands(part):
    if hasattr(part, 'kind'):
        if part.kind == "command":
            buffer = []
            i = 0
            while i < len(part.parts):
                sub = part.parts[i]
                if not (hasattr(sub, "kind") and sub.kind == "word"):
                    if buffer:
                        yield part, buffer
                        buffer = []
                    i += 1
                    continue
                if hasattr(sub, 'parts'):
                    for nested in sub.parts:
                        yield from bashlex_commands(nested)
                buffer.append(sub.word)
                i += 1
            if buffer:
                yield part, buffer
        elif part.kind == "commandsubstitution":
            yield from bashlex_commands(part.command)
        elif part.kind == "list":
            for part in part.parts:
                yield from bashlex_commands(part)

class BuilderContext:
    def __init__(self, image, name=None, directory='/', user='root') -> None:
        self.directory = directory
        self.env = {}
        self.args = {}
        self.name = name
        self.user = user
        self.exposed = []
        self.image = image
        self.loaded = False
        if self.name is None:
            self.name = self.image.name
        self.commands = []
        self.try_load_image_context()
    def to_stage(self):
        return Stage(
            self.image,
            self.commands,
            self.env,
            self.args,
            self.user,
            self.directory,
            self.exposed,
            self.name,
        )
    def dumps(self):
        ret = f"FROM {self.image.id}"
        if self.name != self.image.name:
            ret += " as " + self.name
        ret += "\n"
        for command in self.commands:
            ret += command.line + '\n'
        return ret

    def try_load_image_context(self):
        if os.getuid() != 0:
            return
        try:
            image = self.image.load()
        except Exception as e:
            return
        env = image.attrs['ContainerConfig'].get('Env', ())
        if env: 
            for item in image.attrs['ContainerConfig'].get('Env', ()):
                k, v = item.split('=', 1)
                self.env[k] = v
        ports = image.attrs['ContainerConfig'].get('ExposedPorts', ())
        if ports:
            for port in ports:
                self.exposed.append(EXPOSE.Port.parse(port))
        self.loaded = True
            
    def command_context(self):
        env, args = {}, {} 
        env.update(self.env)
        args.update(self.args)
        return {'path': self.directory, 'env': env, 'args': args, 'user': self.user}

class GenericDockerCommand:

    def __init__(self, command, arg, parser) -> None:
        self.command = command
        self.arg = arg.strip()
        self.kwargs = {}
        self.args = []
        self.parser = parser
        self.__i = -1 if not self.parser or not self.parser.context else len(self.parser.context.commands)
    def _extract_arguments(self):
        # TODO: arguments with `--key="value "` and `--key=val\ ue`
        part, *rest = self.arg.split(' ', 1)
        while part.startswith('--'):
            if '=' not in part:
                self.args.append(part[2:])
                continue
            key, value = part[2:].split('=')
            self.kwargs[key] = value
            if not rest:
                break
            part, *rest = rest[0].split(' ', 1)
        self.arg = ' '.join([part] + rest)

    def parse(self):
        self.parser.context.commands.append(self)
    @property
    def line(self):
        kwargs = ' '.join([f'--{k}={repr(v)}' for k, v in self.kwargs.items()])
        return " ".join((self.command, kwargs, self.arg))
    def __repr__(self):
        return f'<{self.command} "{self.arg}" {self.kwargs}>'

class RUN(GenericDockerCommand):
    def __init__(self, command, arg, parser):
        super().__init__(command, arg, parser)
        self.context = None
        self.parsed = None
    def calls(self):
        if not self.parsed:
            return []
        yield from map(lambda x: x[1], bashlex_commands(self.parsed[0]))
    def parse(self):
        self._extract_arguments()
        self.parsed = bashlex.parse(self.arg)
        self.context = self.parser.context.command_context()
        return super().parse()

class COPY(GenericDockerCommand):
    def __init__(self, command, arg, parser):
        super().__init__(command, arg, parser)
        self.sources = []
        self.destination = None
    def parse(self):
        self._extract_arguments()
        sources, self.destination = self.arg.rsplit(' ', 1)
        self.destination = os.path.join(
            self.parser.context.directory,
            self.destination
        ).rstrip('.')
        if ',' in sources:
            self.sources = sources.split(',')
        else:
            self.sources = [sources]
        return super().parse()
    def __repr__(self):
        return f'<{self.command} {self.args} {self.kwargs} {self.sources} -> {self.destination}>'

class ADD(COPY):
    # TODO: GIT and HTTP sources
    pass


def strip_token(svar, token='"'):
    if not svar or svar[0] != token or svar[-1] != token:
        return svar
    return svar.replace('\\' + token, token)[1:-1]
    
class ENV(GenericDockerCommand):
    rex =  re.compile(r'(\w[^\s=]*)=((?:(?:(?:\\ )|[^\s"])+)|(?:"[^"]*"))')
    def __init__(self, command, arg, parser) -> None:
        super().__init__(command, arg, parser)
        self.variables = {}
    @staticmethod
    def _clean_value(value):
        if not value:
            return value
        if value[0] in ('"', "'"):
            value = strip_token(value, value[0])
        return value.replace('\\ ', ' ')
    @classmethod
    def _arg_to_dict(cls, arg):
        part, *rest = arg.split(' ', 1)
        variables = {}
        if '=' not in part:
            variables[part] = rest[0]
            return variables
        for key, value in cls.rex.findall(arg):
            variables[key] = cls._clean_value(value)
        return variables
    def parse(self):
        self.variables.update(self._arg_to_dict(self.arg))
        self.parser.context.env.update(self.variables)
        return super().parse()
    def __repr__(self):
        return f'<{self.command} {self.args} {self.kwargs} {self.variables}>'

class ARG(GenericDockerCommand):
    def __init__(self, command, arg, parser) -> None:
        super().__init__(command, arg, parser)
        self.key = None
        self.default = None
    def parse(self):
        self.key, self.default = self.arg.strip(), None
        if '=' in self.key:
            self.key, self.default = self.key.split('=', 1)
            self.default = ENV._clean_value(self.default)
        if self.parser.context:
            self.parser.context.args[self.key] = self
            # Use GenericDockerCommand parse base
            return super().parse()
        self.parser.globals[self.key] = self
class WORKDIR(GenericDockerCommand):
    def parse(self):
        self.parser.context.directory = os.path.join(
            self.parser.context.directory,
            self.arg.strip()
        )
        return super().parse()

class FROM(GenericDockerCommand):
    rex = re.compile(
        r'(?:--platform=(?P<platform>[^\s]+)\s)?'  # optional platform argument
        r'\s*(?P<image>[^\s:@]+)'
        r'(?::(?P<tag>[^\s@]+))?'
        r'(?:@(?P<digest>[^\s]+))?'
        r'(?:\s+[aA][sS]\s+(?P<name>[^\s]+))?'
    )
    class Image:
        def __init__(self, name, tag='latest', digest=None, platform=None) -> None:
            self.name = name
            self.tag = tag
            self.digest = digest
            self.platform = platform
        @property
        def id(self):
            iid = self.name
            if self.tag:
                iid += ':' + self.tag
            return iid
        def load(self):
            """Requires sudo"""
            import docker
            client = docker.from_env()
            item = f'{self.name}:{self.tag}'
            try:
                image = client.images.get(item)
            except Exception:
                image = client.images.pull(item)
            return image
        def __repr__(self) -> str:
            return f'<Image {self.name}:{self.tag}>'
    def parse(self):
        match = self.rex.match(self.arg)
        if not match:
            raise ParsingError('From', self.arg)
        groups = match.groupdict()
        if not groups['image']:
            raise ParsingError('From', self.arg)
        image = self.Image(groups['image'], groups['tag'], groups['digest'], groups['platform'])
        if self.parser.context is not None:
            self.parser.stages.append(self.parser.context)
        self.parser.context = BuilderContext(image, groups['name'])

class USER(GenericDockerCommand):
    def __init__(self, command, arg, parser) -> None:
        super().__init__(command, arg, parser)
        self.user = None
        self.group = None
    def parse(self):
        self.user = self.arg
        if ':' in self.user:
            self.user, self.group = self.user.split(':')
        return super().parse()

class EXPOSE(GenericDockerCommand):
    class Port:
        rex = re.compile(r'(\d+)(?:/(tcp|udp))?')
        def __init__(self, port, proto=None) -> None:
            self.port = port
            self.proto = proto
        def __repr__(self) -> str:
            if self.proto:
                return f'{self.port}/{self.proto}'
            return str(self.port)
        @classmethod
        def parse(cls, svar):
            m = cls.rex.match(svar)
            if not m:
                return None
            port, proto = m.groups()
            if not proto:
                proto = None
            port = int(port)
            return cls(port, proto)
    def __init__(self, command, arg, parser) -> None:
        super().__init__(command, arg, parser)
        self.ports=[]
    def parse(self):
        self.ports = []
        for item in self.arg.split():
            exposed = self.Port.parse(item)
            if exposed:
                self.ports.append(exposed)
        self.parser.context.exposed.extend(self.ports)
        return super().parse()

class CMD(GenericDockerCommand):
    rex = re.compile(r'\[?.?\s*(?:("(?:(?:\\")|[^"])+")|(\'(?:(?:\\\')|(?:[^\']))+\'))\s*\]?,?')
    def __init__(self, command, arg, parser) -> None:
        super().__init__(command, arg, parser)
        self._cmd = None
        self.context = {}
    @property
    def cmd(self):
        if type(self._cmd) == list:
            return ' '.join(self._cmd)
        return ' '.join(bashlex_iter(self._cmd))
    def parse(self):
        if self.arg.startswith('[') and self.arg.endswith(']'):
            parts = self.rex.findall(self.arg)
            self._cmd = []
            for part in parts:
                for component in part:
                    if component:
                        self._cmd.append(component.replace('\\' + component[0], component[0])[1:-1])
                        break
        else:
            self._cmd = bashlex.parse(self.arg)[0]
        self.context = self.parser.context.command_context()
        return super().parse()

    def __repr__(self):
        return f'<{self.command} {self.cmd}>'

class ENTRYPOINT(CMD):
    pass

class Parser:
    DOCKER_COMMANDS = {
        'FROM': FROM,
        'RUN': RUN,
        'CMD': CMD,
        'LABEL': GenericDockerCommand,
        'EXPOSE': EXPOSE,
        'ENV': ENV,
        'ADD': ADD,
        'COPY': COPY,
        'ENTRYPOINT': ENTRYPOINT,
        'VOLUME': GenericDockerCommand,
        'USER': USER,
        'WORKDIR': WORKDIR,
        'ARG': ARG,
        'ONBUILD': GenericDockerCommand,
        'STOPSIGNAL': GenericDockerCommand,
        'HEALTHCHECK': GenericDockerCommand,
        'SHELL': GenericDockerCommand,
    } 
    def __init__(self) -> None:
        self.errors = []

        self.commands = []
        self.globals = {}
        self.stages = []
        
        self.resources = []
        self.unique = []

        self.context = None

    def build(self):
        if self.context:
            self.stages.append(self.context)
            self.context = None
        docker = Docker()
        docker.lines = 0
        for stage in self.stages:
            docker.bases.append(stage.image)
            docker.stages.append(stage.to_stage())
            docker.lines += len(stage.commands)
        return docker

    def loadline(self, line):
        # Remove comments and clear surounding whitespace
        line = line.strip()
        if not line or line.startswith('#'):
            return
        cmd, arg = line.split(' ', 1)
        cmd = cmd.upper()
        if cmd not in self.DOCKER_COMMANDS:
            self.errors.append(f'Unknown command "{cmd}"!')
            return
        self.DOCKER_COMMANDS[cmd](cmd, arg, self).parse()

    @classmethod
    def loads(cls, docker_content):
        parser = cls()
        docker_content = docker_content.replace('\\\n', '')
        for line in docker_content.splitlines():
            try:
                parser.loadline(line)
            except Exception as e:
                parser.errors.append(f'Unexpected exception "{e}"!')
                return None
        if not parser.context:
            # Invalid docker with no stages
            return None
        return parser.build()
