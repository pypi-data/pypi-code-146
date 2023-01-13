"""Dict utils like attr and dot-notation access."""

__all__ = [
    "AttrDict",
    "attrify",
    "flatten_dotdict",
    "inflate_dotdict",
    "get_field",
]


class AttrDict(dict):
    """Dictionary allowing attribute access for keys."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize AttrDict from args/kwargs as accepted by the builtin dict."""
        super().__init__({k: attrify(v) for k, v in dict(*args, **kwargs).items()})

    @classmethod
    def from_flat(cls, *args, **kwargs) -> "AttrDict":
        """Return inflated AttrDict: {a.b: c} => {a: {b:c}}."""
        return cls(inflate_dotdict(dict(*args, **kwargs)))

    def to_flat(self) -> dict:
        """Return flattened dict: {a: {b:c}} => {a.b: c}."""
        return flatten_dotdict(self)

    def __getattr__(self, name: str):
        """Get dict key via attribute access."""
        try:
            return self[name]
        except KeyError:
            msg = f"{self.__class__.__name__!r} object has no attribute {name!r}"
            raise AttributeError(msg) from None

    def __setattr__(self, name: str, value) -> None:
        """Set dict key via attribute access."""
        self[name] = value


def attrify(data):
    """Return data with dicts recursively cast to AttrDict in dicts/lists."""
    if isinstance(data, dict):
        return AttrDict(data)
    if isinstance(data, list):
        return [attrify(elem) for elem in data]
    return data


def flatten_dotdict(deep: dict, prefix: str = "") -> dict:
    """Flatten nested dictionary using dot-notation: {a: {b:c}} => {a.b: c}."""
    flat = {}
    for key, value in deep.items():
        key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten_dotdict(value, prefix=key))
        else:
            flat[key] = value
    return flat


def inflate_dotdict(flat: dict) -> dict:
    """Inflate dot-notated dictionary to a nested one: {a.b: c} => {a: {b:c}}."""
    deep = node = {}  # type: ignore
    for key, value in flat.items():
        parts = key.split(".")
        path, key = parts[:-1], parts[-1]
        for part in path:
            node = node.setdefault(part, {})
        node[key] = value
        node = deep
    return deep


def get_field(obj, field: str):
    """Return an object's key/attr with support for nesting/dot-notation."""
    # dot-notated
    try:
        return obj[field]
    except (TypeError, KeyError):
        pass
    try:
        return getattr(obj, field)
    except AttributeError as exc:
        if f"object has no attribute {field!r}" not in exc.args[0]:
            raise
    # nested
    node = obj
    for part in field.split("."):
        try:
            node = node[part]
            continue  # pragma: no cover
        except (TypeError, KeyError):
            pass
        try:
            node = getattr(node, part)
            continue
        except AttributeError as exc:
            if f"object has no attribute {part!r}" not in exc.args[0]:
                raise
        return None
    return node  # pragma: no cover
