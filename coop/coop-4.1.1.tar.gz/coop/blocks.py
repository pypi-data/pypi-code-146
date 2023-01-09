from django.utils.safestring import mark_safe
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock


class UnwrappedStreamBlock(blocks.StreamBlock):
    """Removes the surrounding divs around streamblocks."""

    def render_basic(self, value, context=None):
        return mark_safe('\n'.join(
            child.render(context=context) for child in value))


class LinkValue(blocks.StructValue):
    @property
    def href(self):
        if page := self.get('page'):
            return page.full_url
        elif doc := self.get('document'):
            return doc.url
        url = self.get('url', '')
        return url

    @property
    def text(self):
        if link_text := self.get('link_text'):
            return link_text
        elif page := self.get('page'):
            return page.title
        # Shouldn't get here
        return 'Click here'


class BaseLinkBlock(blocks.StructBlock):
    def render_basic(self, value: LinkValue, context=None):
        return mark_safe(
            f'<a href="{value.href}">{value.text}</a>')


class InternalLink(BaseLinkBlock):
    link_text = blocks.CharBlock(required=False, help_text='Leave blank to use page name')
    page = blocks.PageChooserBlock()

    class Meta:
        value_class = LinkValue
        icon = 'doc-empty'


class ExternalLink(BaseLinkBlock):
    link_text = blocks.CharBlock()
    url = blocks.URLBlock()

    class Meta:
        value_class = LinkValue
        icon = 'fa-external-link'


class DownloadLink(BaseLinkBlock):
    link_text = blocks.CharBlock(help_text='e.g. Download File')
    document = DocumentChooserBlock()

    class Meta:
        value_class = LinkValue
        icon = 'fa-download'


class LinkBlocks(UnwrappedStreamBlock):
    external = ExternalLink()
    internal = InternalLink()
    download = DownloadLink()

    class Meta:
        icon = 'fa-list'
