import datetime
import json
import os
import pathlib
import random
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import lorem_ipsum
from django.utils.text import capfirst
from wagtail.documents.models import Document
from wagtail.images import get_image_model

Image = get_image_model()


n = random.randint


def rbool(prob=0.5):
    return random.random() < prob


def lpar(num):
    """``num`` random paragraphs of lorem ipsum."""
    return ''.join('<p>{0}</p>'.format(p)
                   for p in lorem_ipsum.paragraphs(num, False))


def lwords(num):
    """``num`` random lorem ipsum words."""
    return capfirst(lorem_ipsum.words(num, False))


def tel():
    """ random international format (aus) telephone number eg. +61 (0) 412 345 678"""
    return '+{0} ({1}) {2} {3} {4}'.format(
        n(10, 99), n(0, 9), n(100, 999), n(100, 999), n(100, 999))


def rdate(future=True):
    """
    A random date. Set ``future`` to True for dates in the future, False for
    dates in the past. Possible dates span up to five years from today.
    """
    now = datetime.date.today()
    delta = datetime.timedelta(days=n(0, 1825))
    if future:
        return now + delta
    else:
        return now - delta


def r_heading(level, num):
    return '<h{0}>{1}</h{0}>'.format(level, lwords(num))


def r_bold(num):
    return '<p><b>{0}</b></p>'.format(lwords(num))


def r_italic(num):
    return '<p><i>{0}</i></p>'.format(lwords(num))


def r_ordered_list(list_elements):
    list_elems = []
    for _ in range(list_elements):
        list_elems.append('<li>{0}</li>\n'.format(lwords(n(2, 4))))
    return '<ol>\n{0}</ol>'.format('\n'.join(map(str, list_elems)))


def r_unordered_list(list_elements):
    list_elems = []
    for _ in range(list_elements):
        list_elems.append('<li>{0}</li>\n'.format(lwords(n(2, 4))))
    return '<ul>\n{0}</ul>'.format('\n'.join(map(str, list_elems)))


def hr():
    return '<hr>'


def r_anchor(num):
    return ("<a href='http://example.com'>{0}</a>".format(lwords(num)))


def r_image():
    image = get_random_image()
    return ('<embed alt="Example image" embedtype="image" format="fullwidth" id="{0}"/>'.format(image.id))


def embed_video():
    return '<embed embedtype="media" url="{0}"/>'.format(get_random_video_url())


def rich_text_example():
    """Layout all possible elements that can be used in rich text fields."""
    return open(os.path.join(os.path.dirname(__file__), 'rich_text_example.html'), 'r').read()


def random_rich_text_example(num, embeds=False):
    """
    Layout some possible elements that can be used in rich text fields in a random fashion
    Takes one argument, the number of elements. Set embeds=True if you wish to include images
    and videos
    """
    funcs = [
        lambda: r_heading(n(2, 5), n(1, 3)),
        lambda: r_bold(n(3, 5)),
        lambda: r_italic(n(3, 5)),
        lambda: r_ordered_list(n(3, 5)),
        lambda: r_unordered_list(n(3, 5)),
        lambda: r_anchor(n(3, 5)),
        lambda: lpar(n(3, 5)),
        hr,
    ]
    if embeds:
        funcs.extend([r_image, embed_video])
    return '\n'.join([random.choice(funcs)() for _ in range(num)])


def json_dumps(x):
    """Dump a value to JSON using the Django JSON encoder"""
    return json.dumps(x, cls=DjangoJSONEncoder)


def shuf(l1):
    """Generate a shuffled copy of a list"""
    l2 = l1[:]
    random.shuffle(l2)
    return l2


class once(object):
    """A decorator that only calls the decorated function once"""
    has_run = False
    value = None
    fn = None

    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        if self.has_run:
            return self.value

        self.value = self.fn(*args, **kwargs)
        self.has_run = True
        return self.value


def setup_images(test_img_dir=None):
    def _is_image(filename):
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        return pathlib.Path(filename).suffix.lower() in extensions

    image_prefix = 'original_images/test-images'
    dest_dirname = os.path.join(settings.MEDIA_ROOT, image_prefix)

    if test_img_dir is None:
        HERE = os.path.join(os.path.dirname(__file__))
        test_img_dir = os.path.join(HERE, 'test_images')
    # Copy all images from test_img_dir to dest_dirname
    for filename in os.listdir(test_img_dir):
        image_src_path = os.path.join(test_img_dir, filename)
        image_dest_path = os.path.join(dest_dirname, filename)
        if not default_storage.exists(image_dest_path) and _is_image(filename):
            with open(image_src_path, 'rb') as f:
                default_storage.save(image_dest_path, f)
    # Create Image models for each image in dest_dirname
    for filename in os.listdir(dest_dirname):
        if _is_image(filename):
            image_path = os.path.join(dest_dirname, filename)
            Image.objects.create(title=filename, file=image_path)


def get_random_image(category: str = None) -> Image:
    images = Image.objects.order_by('?')
    if category:
        images = images.filter(tags__name__in=[category])
    return images.first()


def get_image(filename):
    return Image.objects.get(title=filename)


def setup_documents(test_document_dir=None):
    dest_dir = Path(settings.MEDIA_ROOT, 'documents')

    if test_document_dir is None:
        here = Path(__file__).parent.absolute()
        test_document_dir = here.joinpath('test_documents')
    for src_file in test_document_dir.iterdir():
        doc_dest_path = dest_dir.joinpath(src_file.name).as_posix()  # default_storage needs a string
        if not default_storage.exists(doc_dest_path) and src_file.is_file():
            with open(src_file.as_posix(), 'rb') as doc_file:
                default_storage.save(doc_dest_path, doc_file)
    for file in dest_dir.iterdir():
        if file.is_file():
            Document.objects.create(
                title=file.name,
                file=file
            )


def get_random_doc():
    return Document.objects.order_by('?').first()


def get_random_video_url():
    return random.choice([
        'https://youtu.be/H9VVkwRb_7M',
        'https://youtu.be/2WWwkArWajM',
        'https://youtu.be/yYaJWO_mNWs',
        'https://youtu.be/1kThvYlo2Lc',
        'https://youtu.be/Ji9qSuQapFY',
        'https://vimeo.com/155536745',
        'https://vimeo.com/179936131',
        'https://vimeo.com/188197250',
        'https://vimeo.com/175535505',
        'https://vimeo.com/188321226'
    ])


def make_superuser():
    User = get_user_model()
    if User.USERNAME_FIELD == 'email':
        User.objects.create_superuser(email='admin@admin.com', password='p')
    else:
        User.objects.create_superuser(username='admin', email='admin@admin.com', password='p')


def generate_form_streamfield(headings=True, file_field=True):
    """ Generates on field of each possible type """
    basic_types = ['text', 'textarea', 'email', 'number', 'date']

    if headings:
        yield ('heading', 'Basic Types')
    for field_type in basic_types:
        yield ('basic_field', {
            'label': field_type,
            'field_type': field_type,
            'help_text': lwords(10),
            'required': rbool(),
            'default_value': '',
            'placeholder': lwords(2),
        })

    if headings:
        yield ('heading', 'Choice Types')

    choice_types = ['select', 'checkbox', 'radio']

    for field_type in choice_types:
        yield ('choice_field', {
            'label': field_type,
            'field_type': field_type,
            'choices': [lwords(n(1, 2)) for _ in range(n(2, 8))],
            'help_text': lwords(10),
            'required': rbool(),
        })

    if file_field:
        if headings:
            yield ('heading', 'File types')
        yield ('file_field', {
            'label': 'File',
            'help_text': lwords(10),
            'required': rbool(),
        })
