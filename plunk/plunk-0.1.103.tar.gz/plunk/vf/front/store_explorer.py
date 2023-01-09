from dataclasses import dataclass
from functools import partial
import re
from typing import Iterable, List
from streamlitfront import mk_app, binder as b
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from front.crude import Crudifier
from streamlitfront.elements import FileUploader, SuccessNotification
import re
import uuid

from plunk.ap.store_explorer.store_explorer_element import get_mall

SEARCH_MODE_KEYS = 1
SEARCH_MODE_VALUES = 2
SEARCH_MODE_KEYS_AND_VALUES = 3
SEARCH_MODE_PATH = 4

DOUBLE_WILDCARD = str(uuid.uuid4())


_mall = dict(
    search_mode={
        'Keys Only': SEARCH_MODE_KEYS,
        'Values Only': SEARCH_MODE_VALUES,
        'Keys and Values': SEARCH_MODE_KEYS_AND_VALUES,
        'Path': SEARCH_MODE_PATH,
    },
    sound_output=dict(),
    data=dict(
        aaa=1,
        bbb='2',
        ccc=[3],
        ddd={'4': 4, '5': [{'e': 6}, {'f': 7}, ['g', 'h', 'i']]},
        jjj=[{'k': 8, 'l': 9}, 'm', 10],
    ),
)
mall = get_mall(_mall)
crudifier = partial(Crudifier, mall=mall)

WaveForm = Iterable[int]


@crudifier(output_store='sound_output')
def upload_sound(train_audio: List[WaveForm], tag: str):
    return train_audio, tag


@dataclass
class DictExplorer:
    dict_to_explore: dict

    def __call__(
        self,
        search_mode: int,
        search: str,
        match_case: bool = False,
        match_whole_word: bool = False,
        use_regex: bool = False,
    ):
        if not search:
            return self.dict_to_explore

        self.match_case = match_case
        self.match_whole_word = match_whole_word
        self.use_regex = use_regex

        self.search = search if self.match_case else search.lower()

        if not self.search:
            return self.dict_to_explore

        if not self.match_case:
            self.search = search.lower()

        self.search_keys = search_mode in (
            SEARCH_MODE_KEYS,
            SEARCH_MODE_KEYS_AND_VALUES,
            SEARCH_MODE_PATH,
        )
        self.search_values = search_mode in (
            SEARCH_MODE_VALUES,
            SEARCH_MODE_KEYS_AND_VALUES,
        )

        return (
            self._search_path()
            if search_mode == SEARCH_MODE_PATH
            else self._filter_dict_from_str()
        )

    def _search_path(self):
        self.match_whole_word = True
        self.use_regex = True
        self.path = [
            re.sub(  # add a dot before any wildcard with no dot to use it as a regex ('*' -> '.*')
                r'(?<!\.)\*',
                '.*',
                re.sub(  # escape the double wildcards first ('**' -> value of DOUBLE_WILDCARD)
                    r'^\*\*$', DOUBLE_WILDCARD, el
                ),
            )
            for el in re.split(
                r'(?<!\\)\/', self.search
            )  # (?<!\\) is for escaping slash characters using a backslash ('\/')
            if el
        ]
        return self._filter_dict_from_path()

    def _filter_dict_from_path(self, d=None, path=None, double_wildcard=False):
        def build_dict():
            _double_wildcard = double_wildcard
            for k, v in d.items():
                _path_tail = path_tail
                match = False
                if next_el == DOUBLE_WILDCARD:
                    _double_wildcard = True
                else:
                    match = self._include_item(next_el, k)
                    if match:
                        _double_wildcard = False
                    else:
                        _path_tail = [next_el] + path_tail
                if match or _double_wildcard:
                    if isinstance(v, dict):
                        _v = self._filter_dict_from_path(
                            v, _path_tail, _double_wildcard
                        )
                        if _v != {} or (v == {} and not _path_tail):
                            yield k, _v
                    elif not _path_tail:
                        yield k, v

        d = self.dict_to_explore if d is None else d
        path = self.path if path is None else path
        if not path:
            return d
        next_el = path[0]
        path_tail = path[1:]
        return {k: v for k, v in build_dict()}

    def _filter_dict_from_str(self, d=None):
        def build_dict():
            for k, v in d.items():
                if isinstance(v, dict):
                    if self._include_item(self.search, k):
                        yield k, v
                    else:
                        _v = self._filter_dict_from_str(v)
                        if _v:
                            yield k, _v
                elif self._include_item(self.search, k, v):
                    yield k, v

        d = self.dict_to_explore if d is None else d
        return {k: v for k, v in build_dict()}

    def _include_item(self, search, key, value=''):
        _key = str(key)
        _value = str(value)
        if not self.match_case:
            _key = _key.lower()
            _value = _value.lower()
        if self.use_regex:
            regex = f'^{search}$' if self.match_whole_word else search
            return (self.search_keys and re.search(regex, _key)) or (
                self.search_values and re.search(regex, _value)
            )
        else:
            if self.match_whole_word:
                return (self.search_keys and search == _key) or (
                    self.search_values and search == _value
                )
            return (self.search_keys and search in _key) or (
                self.search_values and search in _value
            )


@crudifier(param_to_mall_map=['search_mode'])
def explore_mall(
    search_mode: int,
    search: str,
    match_case: bool = False,
    match_whole_word: bool = False,
    use_regex: bool = False,
):
    dict_explorer = DictExplorer(mall)
    return dict_explorer(
        search_mode=search_mode,
        search=search,
        match_case=match_case,
        match_whole_word=match_whole_word,
        use_regex=use_regex,
    )


# def on_select_search_mode():
#     print(b.selected_search_mode())
#     b.match_whole_word.set(b.selected_search_mode() != 4)


if __name__ == '__main__':

    app = mk_app(
        [upload_sound, explore_mall],
        config={
            APP_KEY: {'title': 'Store Explorer'},
            RENDERING_KEY: {
                'upload_sound': {
                    NAME_KEY: 'Data Loader',
                    'execution': {
                        'inputs': {
                            'train_audio': {
                                ELEMENT_KEY: FileUploader,
                                'type': 'wav',
                                'accept_multiple_files': True,
                            },
                        },
                        'output': {
                            ELEMENT_KEY: SuccessNotification,
                            'message': 'Wav files loaded successfully.',
                        },
                    },
                },
                'explore_mall': {
                    'execution': {
                        # 'inputs': {
                        #     'search_mode': {
                        #         'value': b.selected_search_mode,
                        #         # 'on_value_change': on_select_search_mode,
                        #     },
                        #     'match_whole_word': {
                        #         'value': b.match_whole_word,
                        #         'disabled': b.selected_search_mode() == 'Path'
                        #     }
                        # },
                        'auto_submit': True,
                    }
                },
            },
        },
    )
    app()
