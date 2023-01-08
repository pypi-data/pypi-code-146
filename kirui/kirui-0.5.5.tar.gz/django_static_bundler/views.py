import mimetypes
import posixpath
from importlib.util import find_spec

import sass

from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.http import request, FileResponse, HttpResponse, Http404
from django.utils._os import safe_join
from django.views.static import serve

from django_brython.brython import make_package


def bundle_static_file(request, path):
    path = Path(posixpath.normpath(path).lstrip('/'))

    if path.suffixes[-2:] == ['.scss', '.css']:
        fullpath = find(path.parent / path.stem)
        result = sass.compile(filename=fullpath)

        response = HttpResponse(result, content_type='text/css')
        return response
    elif path.suffixes[-2:] == ['.brython', '.js']:
        module_path = '.'.join(str(path).split('/')[-1].split('.')[:-2])

        try:
            module = find_spec(module_path)
        except ModuleNotFoundError:
            raise Http404(f"'import {module_path}' exception, file: {path} can't be served")

        exclude_modules = getattr(settings, 'BRYTHON_BUNDLER_EXCLUDE', [])
        out = make_package.make(package_name=module.name,
                                package_path=module.submodule_search_locations[0],
                                exclude_modules=exclude_modules)

        return HttpResponse(out, content_type='text/javascript')
        # kirui/core/component.brython.js

    print(path)
    return serve(request, str(path), document_root=settings.STATIC_ROOT)
