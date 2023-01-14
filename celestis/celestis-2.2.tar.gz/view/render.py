import os

def contextualize(html, variables):
    # Fix with a templating engine

    return html

def render_template(file_path, **context):
    with open(file_path) as f:
        template = f.read()
        if os.path.exists(file_path) and not template:
            template = f"<p>The HTML file at {file_path} was empty</p>"

    template = contextualize(template, context)

    return template
    # Templating using Jinja and context.items()
        