from . import AbstractParser
from ...models import AnnotationTarget

class OpenGraph(AbstractParser):
    def parse(self, annotation_target: AnnotationTarget, target_url, bs_document, previous_parse_result):
        # Does not change result if previous parse match
        if previous_parse_result:
            return previous_parse_result

        og_url = bs_document.head.find('meta', property="og:url")
        if og_url is None:
            return False

        og_image = bs_document.head.find('meta', property="og:image")
        if og_image is None:
            return False

        og_title = bs_document.head.find('meta', property="og:title")
        if og_title is None:
            return False

        annotation_target.target = og_url['content']
        annotation_target.image = og_image['content']
        annotation_target.title = og_title['content']

        return True

