from parsel import Selector as _ParselSelector
from scrapyish.response import HTMLResponse


class SelectorList(_ParselSelector.selectorlist_cls):
    pass


class Selector(_ParselSelector):

    __slots__ = ['response']
    selectorlist_cls = SelectorList

    def __init__(self, response=None, text=None, type=None, root=None, **kwargs):
        if response is not None and text is not None:
            raise ValueError(f'{self.__class__.__name__}.__init__() received '
                             'both response and text')
        st = 'html'
        if text is not None:
            response = HTMLResponse(text, st)
        if response is not None:
            text = response.text
            kwargs.setdefault('base_url', response.url)
        self.response = response
        super().__init__(text=text, type=st, root=root, **kwargs)
