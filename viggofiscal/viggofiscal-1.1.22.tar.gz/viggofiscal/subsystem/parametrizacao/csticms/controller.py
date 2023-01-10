import flask
from viggocore.common import exception, utils
from viggocore.common import controller


class Controller(controller.CommonController):

    def __init__(self, manager, resource_wrap, collection_wrap):
        super().__init__(manager, resource_wrap, collection_wrap)

    def list(self):
        filters = self._filters_parse()

        try:
            filters = self._parse_list_options(filters)
            (entities, total_rows) = self.manager.list(**filters)

            page = filters.get('page', None)
            page_size = filters.get('page_size', None)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
        except ValueError:
            raise exception.BadRequest('page or page_size is invalid')

        collection = self._entities_to_dict(
            entities, self._get_include_dicts_vex(filters))

        response = {self.collection_wrap: collection}

        if total_rows is not None:
            response.update({'pagination': {'page': int(page),
                                            'page_size': int(page_size),
                                            'total': total_rows}})

        return flask.Response(response=utils.to_json(response),
                              status=200,
                              mimetype="application/json")
