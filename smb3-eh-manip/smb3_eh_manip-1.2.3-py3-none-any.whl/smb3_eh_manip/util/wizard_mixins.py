"""
The "real" wizard mixins uses sneaky lazy loading (dynamic module imports) for
yaml, which is breaking pyinstaller. I have added it as hiden imports numerous
times to no avail. Adding this a a temporary stopgap to get installers working.

adapted on 12/7/22 from
https://raw.githubusercontent.com/rnag/dataclass-wizard/main/dataclass_wizard/wizard_mixins.py
"""
from typing import Type, Union, AnyStr, List, Optional, TextIO, BinaryIO
import yaml

from dataclass_wizard.bases_meta import DumpMeta
from dataclass_wizard.class_helper import _META
from dataclass_wizard.dumpers import asdict
from dataclass_wizard.enums import LetterCase
from dataclass_wizard.loaders import fromdict, fromlist
from dataclass_wizard.type_def import (
    T,
    Encoder,
    Decoder,
    FileDecoder,
    FileEncoder,
)


class YAMLWizard:
    # noinspection PyUnresolvedReferences
    """
    A Mixin class that makes it easier to interact with YAML data.

    .. NOTE::
      The default key transform used in the YAML dump process is `lisp-case`,
      however this can easily be customized without the need to sub-class
      from :class:`JSONWizard`.

    For example:

        >>> @dataclass
        >>> class MyClass(YAMLWizard, key_transform='CAMEL'):
        >>>     ...

    """

    def __init_subclass__(cls, key_transform=LetterCase.LISP):
        """Allow easy setup of common config, such as key casing transform."""

        # Only add the key transform if Meta config has not been specified
        # for the dataclass.
        if key_transform and cls not in _META:
            DumpMeta(key_transform=key_transform).bind_to(cls)

    @classmethod
    def from_yaml(
        cls: Type[T],
        string_or_stream: Union[AnyStr, TextIO, BinaryIO],
        *,
        decoder: Optional[Decoder] = None,
        **decoder_kwargs
    ) -> Union[T, List[T]]:
        """
        Converts a YAML `string` to an instance of the dataclass, or a list of
        the dataclass instances.
        """
        if decoder is None:
            decoder = yaml.safe_load

        o = decoder(string_or_stream, **decoder_kwargs)

        return fromdict(cls, o) if isinstance(o, dict) else fromlist(cls, o)

    @classmethod
    def from_yaml_file(
        cls: Type[T],
        file: str,
        *,
        decoder: Optional[FileDecoder] = None,
        **decoder_kwargs
    ) -> Union[T, List[T]]:
        """
        Reads in the YAML file contents and converts to an instance of the
        dataclass, or a list of the dataclass instances.
        """
        with open(file) as in_file:
            return cls.from_yaml(in_file, decoder=decoder, **decoder_kwargs)

    def to_yaml(
        self: T, *, encoder: Optional[Encoder] = None, **encoder_kwargs
    ) -> AnyStr:
        """
        Converts the dataclass instance to a YAML `string` representation.
        """
        if encoder is None:
            encoder = yaml.dump

        return encoder(asdict(self), **encoder_kwargs)

    def to_yaml_file(
        self: T,
        file: str,
        mode: str = "w",
        encoder: Optional[FileEncoder] = None,
        **encoder_kwargs
    ) -> None:
        """
        Serializes the instance and writes it to a YAML file.
        """
        with open(file, mode) as out_file:
            self.to_yaml(stream=out_file, encoder=encoder, **encoder_kwargs)

    @classmethod
    def list_to_yaml(
        cls: Type[T],
        instances: List[T],
        encoder: Optional[Encoder] = None,
        **encoder_kwargs
    ) -> AnyStr:
        """
        Converts a ``list`` of dataclass instances to a YAML `string`
        representation.
        """
        if encoder is None:
            encoder = yaml.dump

        list_of_dict = [asdict(o, cls=cls) for o in instances]

        return encoder(list_of_dict, **encoder_kwargs)
