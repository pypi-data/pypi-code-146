class Processor:
    EXTRA = []

    def process_response(self, response):
        raise NotImplementedError()


class Single(Processor):
    def process_response(self, response):
        if len(response) > 0:
            return response[0]

        else:
            return None
