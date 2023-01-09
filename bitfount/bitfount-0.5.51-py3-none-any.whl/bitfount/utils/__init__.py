"""General helpful utilities to be found here."""
from __future__ import annotations

from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
import importlib
import importlib.util
import inspect
from itertools import chain
import linecache
import logging
from pathlib import Path
import random
import sys
from types import ModuleType
from typing import (
    Any,
    Callable,
    DefaultDict,
    Dict,
    Generator,
    Iterable,
    List,
    Literal,
    Mapping,
    NoReturn,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

import docstring_parser
from docstring_parser import DocstringMeta
import numpy as np
from sklearn.preprocessing import OneHotEncoder

__all__: List[str] = [
    "is_notebook",
    "one_hot_encode_list",
    "seed_all",
    "ExampleSegmentationData",
]

from bitfount import config

_logger = logging.getLogger(__name__)

DEFAULT_SEED: int = 42
DOCSTRING_STYLE = docstring_parser.DocstringStyle.GOOGLE


def is_notebook() -> bool:
    """Checks if code is being executed in a notebook or not."""
    try:
        # get_ipython() is always available in a notebook, no need to import
        shell = get_ipython().__class__.__name__  # type: ignore[name-defined] # Reason: captured by NameError # noqa: B950
        return bool(shell == "ZMQInteractiveShell")  # True if ran from Jupyter notebook
    except NameError:
        return False  # Standard Python interpreter


def _inspect_get_file(obj: Any) -> str:
    """This is a wrapper around `inspect.getfile` that works with IPython.

    This is required because `inspect.getfile` does not work with classes defined in a
    notebook due to them not having a `__file__` attribute. Functions in a notebook are
    unaffected.

    Raises:
        TypeError: If the object source code cannot be retrieved.
    """
    # Only classes need a workaround, if the object is not a class we can just fall back
    # to `inspect.getfile`.
    if not inspect.isclass(obj):
        return inspect.getfile(obj)

    # Lookup by parent module as in `inspect.getfile`. This is the flow for classes that
    # are not defined in a notebook.
    if hasattr(obj, "__module__"):
        object_ = sys.modules.get(obj.__module__)
        if object_ is not None and hasattr(object_, "__file__"):
            return str(object_.__file__)

    # If parent module is __main__, lookup by methods. This is the flow for classes that
    # are defined in a notebook.
    for _, member in inspect.getmembers(obj):
        if (
            inspect.isfunction(member)
            and obj.__qualname__ + "." + member.__name__ == member.__qualname__
        ):
            return inspect.getfile(member)

    # If all else fails, raise an error.
    raise TypeError(f"Source for {obj.__name__} not found.")


def _get_ipython_extract_symbols() -> Callable[[Any, Any], Tuple[List, List]]:
    """Returns the `extract_symbols` function from IPython.

    This should only be imported from an environment which has IPython installed.
    """
    from IPython.core.magics.code import (  # type: ignore[import] # Reason: No stubs for this # noqa: B950
        extract_symbols,
    )

    return extract_symbols  # type: ignore[no-any-return] # Reason: No stubs for this # noqa: B950


def _get_object_source_code(obj: Any) -> str:
    """Returns the source code for an object as a string.

    If the object is defined in a file, the function simply returns the result from
    `inspect.getsource`. If the object is defined in a notebook, a different approach
    must be taken to extract the source code.
    """
    if is_notebook():
        extract_symbols = _get_ipython_extract_symbols()

        # Extract the source code from the cell the object is defined in as a string.
        cell_code = "".join(linecache.getlines(_inspect_get_file(obj)))
        # Extracts the first symbol (by name) that is defined in the cell that the
        # object is defined in. This should be the object itself.
        class_code: str = extract_symbols(cell_code, obj.__name__)[0][0]
        return class_code

    return inspect.getsource(obj)


def seed_all(seed_value: Optional[int] = None) -> None:
    """Sets random seed for `numpy`, `python.random` and any other relevant library.

    If `pytorch` is used as the backend, this is just a wrapper around the
    `seed_everything` function from `pytorch-lightning`.

    :::info

    `PYTHONHASHSEED` is not set as an environment variable because this has no effect
    once the process has been started. If you wish to set this, you should set it
    yourself in your own environment before running python.

    :::

    Args:
        seed_value: The seed value to use. If None, uses the default seed (42).
    """
    seed_value = DEFAULT_SEED if seed_value is None else seed_value

    # Try to seed other libraries that may be present
    # Torch
    try:
        import pytorch_lightning as pl

        _logger.debug(f"Setting seed of torch, random and numpy to {seed_value}")
        # This call takes care of setting the seed for all libraries including
        # random and numpy as well as pytorch. `workers=True` ensures that the workers
        # for the dataloaders are also seeded.
        pl.seed_everything(seed_value, workers=True)
    except ModuleNotFoundError:
        _logger.debug(f"Setting seed of random and numpy to {seed_value}")
        random.seed(seed_value)
        np.random.seed(seed_value)


def _add_this_to_list(
    this: Union[Any, Iterable[Any]], the_list: List[Any]
) -> List[Any]:
    """Adds this to the list and returns the list.

    `this` is checked not be `None` or to already exist in `the_list` before it is
    appended. If `this` is an iterable, `the_list` is extended to add the individual
    elements in `this` with the same constraints as just mentioned.

    Args:
        this: The object to add to the list. Can be an iterable.
        the_list: The list to which `this` gets appended to or extended by.

    Returns:
        The list but with any new elements added to the end to ensure the original order
        of the list is preserved.
    """
    if not isinstance(this, Iterable) or isinstance(this, str):
        this = [this]

    for i in this:
        if i is not None and i not in the_list:
            the_list.append(i)

    return the_list


def _array_version(this: Union[Any, Iterable[Any]]) -> List[Any]:
    """Returns this as a list.

    Checks if 'this' is an iterable, in which case it returns it as a list (unless
    it's a string), otherwise it wraps it as a single element list.
    """
    if isinstance(this, Iterable) and not isinstance(this, str):
        return list(this)
    return [this]


def one_hot_encode_list(
    targets: Union[
        np.ndarray, Iterable[np.ndarray], Iterable[int], Iterable[Iterable[int]]
    ]
) -> np.ndarray:
    """Converts a list of targets into a list of one-hot targets."""
    arr_targets: np.ndarray = np.asarray(targets)

    # Can only encode 1D or 2D targets
    if not (1 <= arr_targets.ndim <= 2):
        raise ValueError(
            f"Incorrect number of dimensions for one-hot encoding; "
            f"expected 1 or 2, got {arr_targets.ndim}"
        )

    # OneHotEncoder needs a 2D numpy array so if this is 1D, needs reshape
    if arr_targets.ndim == 1:
        arr_targets = arr_targets.reshape(-1, 1)

    # Ensure output is ndarray of correct types
    encoder = OneHotEncoder(categories="auto", sparse=False, dtype=np.uint8)
    # sparse=False guarantees output of ndarray
    return cast(np.ndarray, encoder.fit_transform(arr_targets))


def _get_module_from_file(path_to_module: Path) -> ModuleType:
    """Creates a module from a file and returns the module.

    :::caution

    This explicitly does NOT add it to sys.modules and hence it is not available
    for import elsewhere. If you want to have the module added to sys.modules, use
    _import_module_from_file instead.

    :::

    Args:
        path_to_module: The path to the module file.

    Returns:
        The module.

    Raises:
        ImportError: If the module cannot be imported.
    """
    path = path_to_module.expanduser().absolute()
    module_name = path.stem

    # Load the module from the file WITHOUT SAVING IT TO sys.modules
    # See: https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly  # noqa: B950
    spec = importlib.util.spec_from_file_location(module_name, path)
    try:
        # `spec` has type `ModuleSpec | None`. If it is None, an error is raised which
        # caught by the `try...except` block
        module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type] # Reason: See comment # noqa: B950
        sys.modules[module_name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr] # Reason: See comment # noqa: B950
    except Exception as ex:
        raise ImportError(f"Unable to load code from {path_to_module}") from ex

    return module


def _import_module_from_file(
    path_to_module: Path, parent_module: Optional[str] = None
) -> Tuple[ModuleType, str]:
    """Imports a module from a file path and returns the module.

    Ensures module is added to sys.modules.

    Args:
        path_to_module: The path to the module file.
        parent_module: The parent module this module should be imported under.

    Returns:
        The module and the base module name (i.e. the module name without any parent
        package elements such as `path` for `os.path`).

    Raises:
        ImportError: If the module cannot be imported.
    """
    path = path_to_module.expanduser().absolute()
    module_name = path.stem

    # Modify module name to reference parent if included
    if parent_module:
        fqual_module_name = f"{parent_module}.{module_name}"
    else:
        fqual_module_name = module_name

    if (existing_module := sys.modules.get(fqual_module_name)) is None:
        _logger.debug(f"Dynamically importing {path_to_module} as {fqual_module_name}")

        # Load the module from the file and import it
        # See: https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly  # noqa: B950
        spec = importlib.util.spec_from_file_location(fqual_module_name, path)
        try:
            # `spec` has type `ModuleSpec | None`. If it is None, an error is raised
            # which is caught by the `try...except` block
            module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type] # Reason: See comment # noqa: B950
            sys.modules[fqual_module_name] = module
            spec.loader.exec_module(module)  # type: ignore[union-attr] # Reason: See comment # noqa: B950
        except Exception as ex:
            # If we added the module to sys.modules, remove it as the import failed
            sys.modules.pop(fqual_module_name, None)  # "None" default prevents KeyError

            raise ImportError(
                f"Unable to load code from {path_to_module} ({str(ex)})"
            ) from ex

        return module, module_name
    else:
        if (
            hasattr(existing_module, "__file__")
            and existing_module.__file__ is not None
            and Path(existing_module.__file__) != path
        ):
            _logger.error(
                "A module with the same name but a different source already exists,"
                " cannot register"
            )
            raise ImportError(
                f"A module with this name already exists: {existing_module}"
            )
        else:
            _logger.debug(
                f"{str(path)} is already loaded as {existing_module.__name__},"
                f" will not reload"
            )
            return existing_module, module_name


def _get_non_abstract_classes_from_module(path_to_module: Path) -> Dict[str, type]:
    """Returns non-abstract classes from a module path.

    Returns a dictionary of non-abstract class names and classes present within a
    module file which is given as a Path object.
    """
    module = _get_module_from_file(path_to_module)

    classes = {
        name: class_
        for name, class_ in vars(module).items()
        if inspect.isclass(class_) and not inspect.isabstract(class_)
    }

    return classes


# TypeVars for merge_list_of_dicts
KT = TypeVar("KT")  # Key type.
VT = TypeVar("VT")  # Value type.


def _merge_list_of_dicts(
    lod: Iterable[Mapping[KT, Union[VT, Iterable[VT]]]]
) -> Dict[KT, List[VT]]:
    """Converts a list of dicts into a dict of lists.

    Each element in the dicts should be a single element or a list of elements.
    Any list of elements will be flattened into the final list, any single
    elements will be appended.

    Args:
        lod: A list of dicts to merge.

    Returns:
        A dictionary of lists where each value is the merged values from the
        input list of dicts.
    """
    # Merge into singular lists rather than a list of dicts
    merged: DefaultDict[KT, List[VT]] = defaultdict(list)

    for i in lod:
        for k, v in i.items():
            # We ignore the mypy errors on the `extend` and `append` calls because
            # we don't know the type of v. Instead rely on the `try...except` block
            # for type safety
            try:
                # Attempt to extend first (for outputs and targets)
                merged[k].extend(v)  # type: ignore[arg-type]  # Reason: will TypeError if not Iterable[VT]  # noqa: B950
            except TypeError:
                # Otherwise if not iterable, append
                v = cast(VT, v)
                merged[k].append(v)

    return merged


@dataclass
class _MegaBytes:
    """Thin wrapper for bytes->MB conversion."""

    whole: int
    fractional: float


def _get_mb_from_bytes(num_bytes: int) -> _MegaBytes:
    """Converts a number of bytes into the number of megabytes.

    Returns a tuple of the number of whole megabytes and the number of megabytes
    as a float.
    """
    mb: float = num_bytes / (1024 * 1024)
    return _MegaBytes(int(mb), mb)


_LOG_LEVELS_STR = Literal[
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
]
_LOG_LEVELS_NUM = Literal[
    50,  # logging.CRITICAL
    40,  # logging.ERROR
    30,  # logging.WARNING
    20,  # logging.INFO
    10,  # logging.DEBUG
]
_LOG_LEVELS = Union[_LOG_LEVELS_STR, _LOG_LEVELS_NUM]


def _find_logger_filenames(
    logger: logging.Logger, level: _LOG_LEVELS
) -> Optional[List[str]]:
    """Finds all files that are being logged to for a given logger and level."""
    # Convert to int-log-level if needed
    if isinstance(level, str):
        level = logging.getLevelName(level)
    level = cast(_LOG_LEVELS_NUM, level)

    # If logger is not enabled for target level, will never output
    if not logger.isEnabledFor(level):
        return None

    # Otherwise, iterate up through the logger hierarchy and note any FileHandler
    # files that will be output to for the target level.
    log_files: List[str] = []
    curr_logger: Optional[logging.Logger] = logger
    while curr_logger:
        handlers = curr_logger.handlers
        log_files.extend(
            h.baseFilename
            for h in handlers
            if isinstance(h, logging.FileHandler) and h.level <= level
        )
        curr_logger = curr_logger.parent  # will be None if root logger

    # Return either the list of file paths or None if no files
    # were found.
    if log_files:
        return log_files
    else:
        return None


_no_tb_limit_sentinel = object()

try:
    import gmpy2  # type: ignore[import] # Reason: see below

    # We only use 2 operations from gmpy2, and we force the output to be int
    HAVE_GMP = True
except ImportError:
    HAVE_GMP = False


def _powmod(base: int, power: int, mod: int) -> int:
    """Computes base^power modulo mod where base, power, mod are integers.

    Uses GMP if available.
    """
    if not HAVE_GMP:
        return pow(base, power, mod)
    else:
        return int(gmpy2.powmod(base, power, mod))


def _powinv(base: int, mod: int) -> int:
    """The multiplicative inverse of base in the integers modulo mod.

    Uses GMP if available.
    """
    if HAVE_GMP:
        try:
            inv = int(gmpy2.invert(base, mod))
            # According to documentation, gmpy2.invert might return 0 on
            # non-invertible element, although it seems to actually raise an
            # exception. To make sure that zero is not returned, we raise an exception
            if inv == 0:
                raise ZeroDivisionError("No inverse exists")
            return inv
        except ZeroDivisionError:
            return pow(base, -1, mod)
    else:
        return pow(base, -1, mod)


@contextmanager
def _full_traceback() -> Generator[None, None, None]:
    """Temporarily sets tracebacklimit to original limit."""
    # If sys.tracebacklimit has been set, we need to store its current value
    orig_limit: Union[int, object]
    try:
        orig_limit = sys.tracebacklimit
    except AttributeError:
        orig_limit = _no_tb_limit_sentinel

    try:
        # Reset traceback limit to default (done by deleting the attribute)
        if orig_limit is not _no_tb_limit_sentinel:
            del sys.tracebacklimit

        yield
    finally:
        # Set back to original value again if needed
        if orig_limit is not _no_tb_limit_sentinel:
            sys.tracebacklimit = cast(int, orig_limit)


_fatal_logger = logging.getLogger("bitfount.fatal")


def _handle_fatal_error(
    ex: Exception,
    logger: logging.Logger = _fatal_logger,
    log_msg: Optional[str] = None,
) -> NoReturn:
    """Determines how to handle fatal errors depending on configuration.

    How the error is handled will depend on the configuration:
        - Normal, API-based use:
            - Exception is raised and system errors out.
            - Limited stack trace/error logged at CRITICAL.
            - Full stack trace logged at DEBUG.

        - Dev, API-based use:
            - Exception is raised and system errors out.
            - Full stack trace logged at CRITICAL.

        - Normal, CLI-based use:
            - Exception is captured and sys.exit() is called.
            - Limited stack trace/error logged at CRITICAL.
            - Full stack trace logged at DEBUG.

        - Dev, CLI-based use:
            - Exception is captured and sys.exit() is called.
            - Full stack trace logged at CRITICAL.

    Dev mode functionality can be configured by setting the BITFOUNT_DEV_MODE
    environment variable to True.
    CLI mode functionality can be configured by setting the BITFOUNT_CLI_MODE
    environment variable to True. This is automatically done if the Bitfount library
    is called from any of the CLI scripts provided.

    Args:
        ex: The exception to handle.
        logger: The logger to use for logging out details. If not provided a
            "bitfount.fatal" logger is used.
        log_msg: The log message to use. If not provided the str() representation
            of the exception is used.
    """
    # Create log_msg from exception if one not explicitly provided
    if not log_msg:
        log_msg = str(ex)

    # Determine how full stack trace will be logged
    if not config.BITFOUNT_DEV_MODE:
        # Will want to say "see debug log for more details"
        additional_log_msg = ""
        if debug_log_files := _find_logger_filenames(logger, "DEBUG"):
            if not log_msg.endswith("."):
                additional_log_msg += "."
            debug_log_files_str = ", ".join(debug_log_files)
            additional_log_msg += f" Full details logged to {debug_log_files_str}."
        logger.critical(log_msg + additional_log_msg)
        with _full_traceback():
            logger.debug(log_msg, exc_info=ex)
    else:
        with _full_traceback():
            logger.critical(log_msg, exc_info=ex)

    if config._BITFOUNT_CLI_MODE:
        # Exit instead of raising exception
        sys.exit(ex)
    else:
        # Exceptions get raised
        raise ex


# Example segmentation image dataset class
class ExampleSegmentationData:
    """A synthetic segmentation dataset example.

    This class is used mainly in Tutorial 10 and testing.
    """

    def masks_to_colorimg(self, masks: np.ndarray) -> np.ndarray:
        """Adds RGB coloring to masks.

        Args:
            masks: The masks to which we want to add coloring.

        Returns:
              The masks with RGB coloring applied to them.
        """
        colors = np.asarray(
            [(201, 58, 64), (242, 207, 1)]
        )  # , (0, 152, 75)])#, (101, 172, 228),(56, 34, 132), (160, 194, 56)])

        colorimg = np.ones((masks.shape[1], masks.shape[2], 3), dtype=np.float32) * 255
        channels, height, width = masks.shape
        for y in range(height):
            for x in range(width):
                selected_colors = colors[masks[:, y, x] > 0.5]

                if len(selected_colors) > 0:
                    colorimg[y, x, :] = np.mean(selected_colors, axis=0)

        return colorimg.astype(np.uint8)

    def generate_data(
        self, height: int, width: int, count: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Generate random data given height, weight and count.

        Args:
            height: The height of the images to generate.
            width: The width of the images to generate.
            count: The number of images to generate.
        """
        x, y = zip(
            *[self._generate_img_and_mask(height, width) for i in range(0, count)]
        )

        X = np.asarray(x) * 255
        X = X.repeat(3, axis=1).transpose([0, 2, 3, 1]).astype(np.uint8)
        Y = np.asarray(y)
        return X, Y

    def _generate_img_and_mask(
        self, height: int, width: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Creates image and mask given height and width."""
        shape = (height, width)
        # Assign random location to triangle and circle
        triangle_location = self._get_random_location(*shape)
        circle_location2 = self._get_random_location(*shape, zoom=1.5)

        # Create input image
        arr = np.zeros(shape, dtype=bool)
        arr = self._add_triangle(arr, *triangle_location)
        arr = self._add_circle(arr, *circle_location2, fill=True)
        arr = np.reshape(arr, (1, height, width)).astype(np.float32)

        # Create target masks
        masks = np.asarray(
            [
                self._add_circle(
                    np.zeros(shape, dtype=bool), *circle_location2, fill=True
                ),
                self._add_triangle(np.zeros(shape, dtype=bool), *triangle_location),
            ]
        ).astype(np.float32)
        return arr, masks

    def _get_random_location(
        self, height: int, width: int, zoom: float = 1.0
    ) -> Tuple[int, int, int]:
        """Gets a random location for placing shapes."""
        x = int(
            width * random.uniform(0.1, 0.9)  # nosec [B311: random] # reason: see below
        )
        y = int(
            height
            * random.uniform(0.1, 0.9)  # nosec [B311: random] # reason: see below
        )
        size = int(
            min(width, height)
            * random.uniform(0.06, 0.12)  # nosec [B311: random] # reason: see below
            * zoom
        )
        # We only use random for generating a images for a demo segmentation
        # dataset used in testing an as an example in tutorial 11
        return (x, y, size)

    def _add_triangle(self, arr: np.ndarray, x: int, y: int, size: int) -> np.ndarray:
        """Adds a triangle to the input arrays."""
        s = int(size / 2)
        triangle = np.tril(np.ones((size, size), dtype=bool))
        arr[
            x - s : x - s + triangle.shape[0], y - s : y - s + triangle.shape[1]
        ] = triangle
        return arr

    def _add_circle(
        self, arr: np.ndarray, x: int, y: int, size: int, fill: bool = False
    ) -> np.ndarray:
        """Adds a circle to the input arrays."""
        xx, yy = np.mgrid[: arr.shape[0], : arr.shape[1]]
        circle = np.sqrt((xx - x) ** 2 + (yy - y) ** 2)
        new_arr = np.logical_or(
            arr,
            np.logical_and(circle < size, circle >= size * 0.7 if not fill else True),
        )
        return new_arr


# Type var for class
_C = TypeVar("_C", bound=Type)


def delegates(
    keep: bool = False, exclude_doc_meta: Optional[List[Any]] = None
) -> Callable[[_C], _C]:
    """Decorator to replace `**kwargs` in signature.

    The `@delegates()` decorator should be added to all classes that inherit
    from a parent class. It will ensure that the signature of the class
    includes all the arguments from the parent class(es) as well as combine
    the docstring of all the parent classes to make sure all args, attributes
    and errors are reflected in the class it decorates.
    """

    def _decorate_class(klass: _C) -> _C:
        # Mypy complains that DocstringMeta is not iterable, when it is,
        # hence the "type: ignore"s.

        # get the signature of the decorated class
        from_klass = klass.__init__
        init_sig = inspect.signature(from_klass)
        init_params = dict(init_sig.parameters)

        # get the docstring of the decorated class
        klass_doc = docstring_parser.parse(
            klass.__doc__ if klass.__doc__ else "", style=DOCSTRING_STYLE
        )

        # aux variables to keep track of everything
        # "combined" keeps track of all args, attributes and errors across all classes.
        combined: DefaultDict[Type[DocstringMeta], List[DocstringMeta]] = defaultdict(
            list
        )
        # "metas" keeps track of all args, attributes and errors for one class only.
        metas: DefaultDict[Type[DocstringMeta], List[DocstringMeta]] = defaultdict(list)
        # "arg_names" keeps track of all the arg (also attrs & errors)
        # names to ensure there are no duplicates.
        arg_names: List[str] = []

        # get all the metadata from the decorated class' docstring and...
        for meta in klass_doc.meta:
            meta_type = type(meta)
            if exclude_doc_meta is not None:
                if meta_type in exclude_doc_meta:
                    continue
            metas[meta_type].append(meta)
        # ...feed it into our aux variables
        for (meta_type, meta_list) in metas.items():
            combined[meta_type].extend(meta_list)
            arg_names += [arg.args[1] for arg in meta_list]

        if "kwargs" in init_params:
            init_kwargs = init_params.pop("kwargs")
        else:
            init_kwargs = None

        # We only need the ancestors from our own repo.
        ancestors = [
            ancestor
            for ancestor in klass.__mro__
            if ancestor.__module__.startswith("bitfount") and ancestor != klass
        ]
        # ancestors.sort(key=lambda x: len(x.__module__.split(".")))

        # now we loop through all the base classes of the
        # decorated class and extract the relevant items
        for ancestor in ancestors:
            # Load public methods from parent classes

            # pdoc checks whether the methods are in the class's dictionary,
            # so we need to add them to the relevant class to ensure they
            # show up in the docs.
            to_klass_dict = ancestor.__dict__
            # get the abstract methods
            if hasattr(ancestor, "__abstractmethods__"):
                abstract_methods = ancestor.__abstractmethods__  # type: ignore[attr-defined] # Reason: hasattr check # noqa: B950
            else:
                abstract_methods = []

            # Get the public non-abstract attributes
            new_dict_items = {
                attr_name: attr
                for attr_name, attr in to_klass_dict.items()
                if not attr_name.startswith("_")
                and attr_name not in klass.__dict__
                and attr_name not in abstract_methods
            }

            for attr_name, attr in new_dict_items.items():
                # `If` checks below explained:
                # 1. We only need to document the methods from bitfount modules.
                # 2. Only get the public methods from parent classes.
                # 3. Check if the methods is not already in the class's dictionary.
                # 4. Only get callables (i.e. functions).
                # This will no affect in any way the error
                # handling for abstract methods not being implemented.
                if (
                    ancestor.__module__.startswith("bitfount")
                    and not attr_name.startswith("_")
                    and attr_name not in klass.__dict__
                    and callable(to_klass_dict[attr_name])
                ):
                    # `__dict__` is a mappingproxy which cannot be
                    # updated in the same way we would update a
                    # dictionary, so need the setattr instead.
                    setattr(klass, attr_name, attr)

            # get the docstring and the metadata
            item_doc = docstring_parser.parse(
                ancestor.__doc__ if ancestor.__doc__ else "", style=DOCSTRING_STYLE
            )

            # "metas" keeps track of all args, attributes and errors for one class only.
            metas = defaultdict(list)  # reset to empty
            for meta in item_doc.meta:
                meta_type = type(meta)
                if exclude_doc_meta is not None:
                    if meta_type in exclude_doc_meta:
                        continue
                metas[meta_type].append(meta)
            # keep track in aux variables
            for (meta_type, meta_list) in metas.items():
                to_add = [arg for arg in meta_list if arg.args[1] not in arg_names]
                arg_names += [arg.args[1] for arg in meta_list]
                combined[meta_type].extend(to_add)

            # now sort alphabetically the args, attrs
            # and errors in the docstring.
            # NOTE: have to sort in place in order to keep the defaultdict
            for k, v in combined.items():
                combined[k] = sorted(v, key=lambda d: d.args[1])

            # Now get the signature.
            to_klass = ancestor.__init__  # type: ignore[misc] # Reason: _can_ access __init__ directly # noqa: B950
            # extract the "self" param from the signature
            self_param = init_params.pop("self")
            # get the values without default first
            s1 = {
                param_name: param
                for param_name, param in inspect.signature(to_klass).parameters.items()
                if param.default == inspect.Parameter.empty
                and param_name not in init_params
                and param_name not in ["args", "kwargs"]
            }
            # "self" needs to go first, then unparametrised args
            # and then all the other args otherwise an error is raised.
            init_params = {"self": self_param, **s1, **init_params}
            # Then add the params which have default values.
            s2 = {
                param_name: param
                for param_name, param in inspect.signature(to_klass).parameters.items()
                if param.default != inspect.Parameter.empty
                and param_name not in init_params
            }

            init_params.update(s2)

        # Check if kwargs should be kept in the signature
        if keep and init_kwargs is not None:
            init_params["kwargs"] = init_kwargs

        # replace the decorated class's signature.
        from_klass.__signature__ = init_sig.replace(parameters=init_params.values())  # type: ignore[arg-type] # Reason: see below # noqa: B950
        # Mypy complains that Argument "parameters" to "replace" of
        # "Signature" has incompatible type "dict_values[str, Parameter]";
        # expected "Union[Sequence[Parameter], Type[_void], None], even though
        # Signature.replace is untyped.

        # Now, replace the decorated class's docstring metadata.
        klass_doc.meta = list(chain(*combined.values()))
        klass.__doc__ = docstring_parser.compose(klass_doc, style=DOCSTRING_STYLE)

        return klass

    return _decorate_class
