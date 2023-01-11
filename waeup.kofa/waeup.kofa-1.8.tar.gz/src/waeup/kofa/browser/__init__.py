import os

#from waeup.kofa.browser.layout import (
#    KofaPage, KofaForm, KofaLayout, KofaDisplayFormPage, KofaEditFormPage,
#    KofaAddFormPage, NullValidator)
#from waeup.kofa.browser.pages import ContactAdminForm

IMAGE_PATH = os.path.join(
    os.path.dirname(__file__),
    'static'
    )

#: Filesystem paths to default images
DEFAULT_IMAGE_PATH = os.path.join(IMAGE_PATH, 'placeholder.jpg')
DEFAULT_PASSPORT_IMAGE_PATH = os.path.join(IMAGE_PATH, 'placeholder.jpg')
