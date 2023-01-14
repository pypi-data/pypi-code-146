import os
import json

celestis_content = r'''import socket
from celestis.controller import request as rq
from error import *
import os
import signal

def parse_request(request):
    if request == "":
        return "GET", "/", ""
    lines = request.split("\n")
    method, path, headers = lines[0].split(" ")
    headers = dict(line.split(": ") for line in lines[1:-2])
    return method, path, headers

def parse_form(headers):
    if "Content-Type" not in headers:
        return {}
    if headers["Content-Type"] != "application/x-www-form-urlencoded":
        return {}
    return dict(pair.split("=") for pair in headers["Content-Length"].split("&"))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 8080))
sock.listen(8080)

def handle_sigint(signal, frame):
    if conn:
        conn.close()
    sock.close()

    print("Your server has been closed. Thanks for connecting!")

    exit(0)

signal.signal(signal.SIGINT, handle_sigint)

conn = False

print("Celestis server is listening at port 8080...\nTo close the server, visit http://localhost:8080 and then press Ctrl-C on the terminal")

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode("utf-8")

    method, path, headers = parse_request(request)
    form = parse_form(headers)
    response = rq.handle_request(os.getcwd(), path, method, form)
    conn.sendall(response.encode("utf-8"))
    conn.close()
'''

urls_page_content = '''
# urls for the {} project\n
urls = [("/", "home")]
'''

views_page_content = '''
# views for {} project\n
def home():\n
    return "<h1>{} says hi!</h1>"
'''

def create_app(name):
    # Create the app folder
    app_folder = name
    os.makedirs(app_folder, exist_ok=True)
    
    # Create the views.py file
    views_path = os.path.join(app_folder, "views.py")
    with open(views_path, "w") as f:
        f.write(views_page_content.format(name, name))
    
    # Create the urls.py file
    urls_path = os.path.join(app_folder, "urls.py")
    with open(urls_path, "w") as f:
        f.write(urls_page_content.format(name))

    celestis_path = os.path.join(app_folder, "server.py")
    with open(celestis_path, "w") as f:
        f.write(celestis_content)
    
    meta_path = os.path.join(app_folder, "meta.json")
    with open(meta_path, "w") as f:
        data = {
            "project": name,
            "path": os.path.join(os.getcwd(), app_folder)
        }
        json.dump(data, f)
    