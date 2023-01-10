from dataclasses import dataclass
from looqbox.global_calling import GlobalCalling


@dataclass
class I18nManager:
    language: str = None
    vocabulary = dict()

    def __post_init__(self) -> None:
        object.__setattr__(self, "language", GlobalCalling.looq.language if self.language is None else self.language)

    def __getitem__(self, name: str) -> any:
        return getattr(self, name)

    def __setitem__(self, name: str, value: any) -> None:
        return setattr(self, name, value)

    def add_label(self, label_vocabulary: dict) -> None:

        self.vocabulary.update(label_vocabulary)

        self._check_missing_keys()

        for label, term in self.vocabulary.get(self.language, {}).items():
            self._set_keys_as_parameters(label, term)

    def _set_keys_as_parameters(self, label_key: str, label_vocabulary: str) -> None:
        setattr(self, label_key, label_vocabulary)

    def _check_missing_keys(self) -> None:
        for language_ref in self.vocabulary.keys():
            for language in self.vocabulary.keys():
                if not self._have_same_keys(language, language_ref):
                    missing_key = self._get_missing_keys(language, language_ref)
                    raise Exception("Labels does match for all languages.\n" +
                                    f"The following key(s) is missing: {' , '.join(missing_key)}")

    def _have_same_keys(self, language: str, language_ref: str) -> bool:
        return set(self.vocabulary[language_ref]) == set(self.vocabulary[language])

    def _get_missing_keys(self, language: str, language_ref: str) -> set:
        return set(self.vocabulary[language_ref]) ^ set(self.vocabulary[language])
