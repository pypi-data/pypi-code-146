class JijaORMConfigTypeError(TypeError):
    APPS_MESSAGE = 'Apps must be list or tuple of jija_orm.config.App'
    CONNECTION_MESSAGE = 'Connection must be jija_orm.config.Connection, not '

    def __init__(self, *, apps=None, app=None, connection=None):
        if connection:
            super().__init__(f'Connection must be jija_orm.config.Connection, not {type(connection)}')
        else:
            error_type = None
            if app:
                error_type = f'app: {type(app)}'

            if apps:
                error_type = f'apps: {type(apps)}'

            super().__init__(f'{self.APPS_MESSAGE}, got {error_type}')


class AppConfigTypeError(TypeError):
    def __init__(self, models):
        super().__init__(f'Models must be list or tuple, not {type(models)}')


class AppConfigImportError(ImportError):
    def __init__(self, models_module):
        super().__init__(f'Cant import {models_module}')


class TemplateAttributeError(AttributeError):
    def __init__(self, model, field):
        super().__init__(f'{model} does not have {field} field')


class SelectorTypeError(TypeError):
    def __init__(self, template):
        super().__init__(f'Invalid type of selector argument: {template}')
