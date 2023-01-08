from django.core.paginator import Page as BasePage, EmptyPage, Paginator as BasePaginator


class Page(BasePage):
    def next_page_number(self):
        try:
            return self.paginator.validate_number(self.number + 1)
        except EmptyPage:
            return ''

    def previous_page_number(self):
        try:
            return self.paginator.validate_number(self.number - 1)
        except EmptyPage:
            return ''


class Paginator(BasePaginator):
    def _get_page(self, *args, **kwargs):
        return Page(*args, **kwargs)
