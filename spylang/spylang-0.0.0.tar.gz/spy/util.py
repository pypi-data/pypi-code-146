class MagicExtend:
    """
    Create a magic @extend decorator which allows to easily monkey patch
    classes of a given module. The intended usage is the following:

    # in module a.py
    from .util import MagicExtend

    extend = MagicExtend()

    @extend.register
    class Foo:
        pass

    @extend.register
    class Bar:
        pass

    # in module b.py
    import a
    @a.extend
    class Foo:
        x = 42

    @a.extend
    class Bar:
        y = 43
    """

    def __init__(self, modname):
        self.modname = modname
        self.classes = {}

    def __repr__(self):
        return f'<MagicExtend {self.modname!r}>'

    def register(self, cls):
        self.classes[cls.__name__] = cls
        return cls

    def dump_skeleton(self):
        """
        Dump a template skeleton to extend all the registered classes
        """
        lines = []
        w = lines.append
        package, mod = self.modname.rsplit('.', 1)
        w(f'from {package} import {mod}')
        w('')
        for name, cls in self.classes.items():
            w(f'@{mod}.extend')
            w(f'class {name}:')
            w(f'    pass')
            w('')
            w('')
        return '\n'.join(lines)

    def __call__(self, new_class):
        """
        This is the @extend decorator
        """
        name = new_class.__name__
        if name not in self.classes:
            raise AttributeError(f'class {name} is not registered as extendable')
        cls = self.classes[name]
        for key, value in new_class.__dict__.items():
            if key not in ('__dict__', '__doc__', '__module__', '__weakref__'):
                setattr(cls, key, value)
        return cls
