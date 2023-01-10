from viggocore.common.subsystem import manager, entity
from sqlalchemy import func, and_, or_
from datetime import datetime as datetime1
import datetime as datetime2


class CommonManager(manager.Manager):

    def __init__(self, driver):
        super(CommonManager, self).__init__(driver)

    def apply_filters_includes(self, query, dict_compare, **kwargs):
        for id, resource in dict_compare.items():
            for k, v in kwargs.items():
                if id in k and hasattr(resource, k.split('.')[-1]):
                    k = k.split('.')[-1]
                    isinstance_aux = isinstance(v, str)

                    if k == 'tag':
                        # TODO(JorgeSilva): definir o caractere para split
                        values = v
                        if len(v) > 0 and v[0] == '#':
                            values = v[1:]
                        values = values.split(',')
                        filter_tags = []
                        for value in values:
                            filter_tags.append(
                                getattr(resource, k)
                                .like('%#'+str(value)+' %'))
                        query = query.filter(or_(*filter_tags))
                    elif isinstance_aux and self.__isdate(v):
                        day, next_day = self.__get_day_and_next_day(v)
                        query = query.filter(
                            and_(
                                or_(getattr(resource, k) < next_day,
                                    getattr(resource, k) == None),  # noqa: E711
                                or_(getattr(resource, k) >= day,
                                    getattr(resource, k) == None)))  # noqa: E711 E501
                    elif isinstance_aux and '%' in v:
                        normalize = func.viggocore_normalize
                        query = query.filter(normalize
                                             (getattr(resource, k))
                                             .ilike(normalize(v)))
                    else:
                        query = query.filter(getattr(resource, k) == v)

        return query

    def apply_filters(self, query, resource, **kwargs):
        for k, v in kwargs.items():
            if '.' not in k and hasattr(resource, k):
                isinstance_aux = isinstance(v, str)

                if k == 'tag':
                    # TODO(JorgeSilva): definir o caractere para split
                    values = v
                    if len(v) > 0 and v[0] == '#':
                        values = v[1:]
                    values = values.split(',')
                    filter_tags = []
                    for value in values:
                        filter_tags.append(
                            getattr(resource, k)
                            .like('%#'+str(value)+' %'))
                    query = query.filter(or_(*filter_tags))
                elif isinstance_aux and self.__isdate(v):
                    day, next_day = self.__get_day_and_next_day(v)
                    query = query.filter(
                        and_(
                             or_(getattr(resource, k) < next_day,
                                 getattr(resource, k) == None),  # noqa: E711
                             or_(getattr(resource, k) >= day,
                                 getattr(resource, k) == None)))  # noqa: E711
                elif isinstance_aux and '%' in v:
                    normalize = func.viggocore_normalize
                    query = query.filter(normalize(getattr(resource, k))
                                         .ilike(normalize('%'+str(v))))
                elif isinstance(v, str) and '':
                    query = query.filter(
                    )
                else:
                    query = query.filter(getattr(resource, k) == v)

        return query

    def with_pagination(self, **kwargs):
        require_pagination = kwargs.get('require_pagination', False)
        page = kwargs.get('page', None)
        page_size = kwargs.get('page_size', None)

        if (page and page_size is not None) and require_pagination is True:
            return True
        return False

    def __isdate(self, data, format="%Y-%m-%d"):
        res = True
        try:
            res = bool(datetime1.strptime(data, format))
        except ValueError:
            res = False
        return res

    def __get_day_and_next_day(self, data, format="%Y-%m-%d"):
        day = datetime1.strptime(data, format)
        next_day = day + datetime2.timedelta(days=1)
        return (day, next_day)

    def apply_filter_de_ate(self, resource, query, de, ate):
        inicio = datetime1.strptime(de, entity.DATE_FMT)
        fim = datetime1.strptime(ate, entity.DATE_FMT) +\
            datetime2.timedelta(days=1)
        return query.filter(
            and_(resource.created_at > inicio, resource.created_at < fim))
