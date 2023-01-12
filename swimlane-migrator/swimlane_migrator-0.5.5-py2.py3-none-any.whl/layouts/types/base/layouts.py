class layouts(object):

    def __init__(self, layout_obj, config):
        self.layout_obj = layout_obj
        self.logger = config.pop('logger', None)
        self.swimlane_source = config.pop('swimlane_source', None)
        self.swimlane_target = config.pop('swimlane_target', None)

        if self.logger is None:
            raise  Exception('You must provide a logger object')

        if self.swimlane_source is None:
            raise  Exception('You must provide a swimlane_source object')

        if self.swimlane_target is None:
            raise  Exception('You must provide a swimlane_target object')

        self.failed_fields = []

        self.updates_made = False

        self.logger.debug('Working on layout: {}'.format(layout_obj['name']))