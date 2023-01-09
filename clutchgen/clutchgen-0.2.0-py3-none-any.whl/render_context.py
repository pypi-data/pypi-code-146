__default_render_context = {}


def set_default_render_context(params):
    __default_render_context.update(params)


def get_render_context(overwrite_params: dict):
    copy_of_params = __default_render_context.copy()
    copy_of_params.update(overwrite_params)
    return copy_of_params
