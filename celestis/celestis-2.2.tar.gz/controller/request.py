import os
import importlib.util
import re

def extract_function(urls_content, url):
    # urls = ast.literal_eval(urls_content)
    match = re.search(r"urls = (\[.+\])", urls_content)
    if not match:
        return False

    urls = eval(match.group(1))
    for u in urls:
        if u[0] == url:
            return u[1]
    return False

def change_path_format(path):
    components = path.split(os.path.sep)

    dot_string = ".".join(components)
    return dot_string

def get_view(url, project_path):
    urls_path = os.path.join(project_path, "urls.py")

    if not os.path.exists(urls_path):
        return False

    with open(urls_path, "r") as f:
        contents = f.read()

    class_name = extract_function(contents, url)
    views_path = os.path.join(project_path, "views.py")
    spec = importlib.util.spec_from_file_location("views", str(views_path))
    views_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(views_module)

    view_func = getattr(views_module, class_name)

    return view_func()

def handle_request(project_name, path, method, form):
    # Handle the root route
    try:
        response_body = get_view(path, project_name)
    except:
        return "HTTP/1.1 404 Not Found\nContent-Type: text/plain\nContent-Length: 9\n\nNot Found"

    if not response_body:
        return "HTTP/1.1 404 Not Found\nContent-Type: text/plain\nContent-Length: 9\n\nNot Found"

    return "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n\n{}".format(len(response_body), response_body)
