from flask import Flask
from . import config
app = Flask('genesys')

from genesys.app.blueprints.index.routes import index
from genesys.app.blueprints.project.routes import project
from genesys.app.blueprints.task.routes import task
from genesys.app.blueprints.asset.routes import asset
from genesys.app.blueprints.refresh.routes import refresh


app.register_blueprint(index)
app.register_blueprint(project)
app.register_blueprint(task)
app.register_blueprint(asset)
app.register_blueprint(refresh)
app.config.from_object(config)
