"""Класс, предоставляющий базовый набор функция для управления файлами сервера."""
import os
import sys
import html
import urllib

from .constants import TYPES
from .classes import Response, File


def manage_files(request, allow_dirs=True) -> Response | tuple[int, str]:
    """Функция возвращает с сервера файл, запрашиваемый пользователем.

    Args:
        request (Request): входящий запрос пользователя
        allow_dirs (bool, optional): разрешать пользователю просматривать \
            содержимое директорий. Defaults to True

    Returns:
        Response: сформированный ответ
    """
    path = '.' + request.path
    ext = path.split('.', -1)[-1]
    if os.path.exists(path):
        if os.path.isdir(path) and allow_dirs:
            return _list_directory(path)
        if os.path.isfile(path) or os.path.islink(path):
            return Response(
                200,
                File(path, path[2:]),
                content_type=ext if ext in TYPES else "bin")
        return 500, 'Error: unknown object type.'
    return 404, "Error: file not found."


def _list_directory(path):
    file_list = os.listdir(path)
    file_list.sort(key=lambda a: a.lower())
    enc = sys.getfilesystemencoding()
    res = f"""
    <!DOCTYPE HTML>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset={enc}">
            <title>Directory listing for {path}</title>
            <body>
                <h1>Directory listing for {path}</h1>
                <hr>
                    <ul>
    """

    for name in file_list:
        fullname = os.path.join(path, name)
        display_name = link_name = name
        if os.path.isdir(fullname):
            display_name = name + "/"
            link_name = name + "/"
        if os.path.islink(fullname):
            display_name = name + "@"
        res += f"""
                        <li>
                            <a href="{urllib.parse.quote(link_name,errors="surrogatepass")}">
                            {html.escape(display_name, quote=False)}
                            </a>
                        </li>"""

    res += """
                </ul>
            <hr>
        </body>
    </html>"""
    return Response(200, res)
