import os

views_content = '''
# views for {} project
'''

urls_content = '''
# urls for {} project
'''

server_code = ''

def create_app(project_name):
    os.makedirs(project_name, exist_ok=True)

    views_path = os.path.join(project_name, "views.py")
    with open(views_path, "w") as f:
        f.write(views_content.format(project_name))
    
    urls_path = os.path.join(project_name, "urls.py")
    with open(urls_path, "w") as f:
        f.write(urls_content.format(project_name))
    
    server_path = os.path.join(project_name, "server.py")
    with open(server_code) as f:
        f.write(server_code)
    
    
    