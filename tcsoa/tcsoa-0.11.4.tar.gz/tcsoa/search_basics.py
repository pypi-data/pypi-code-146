from typing import Optional, Dict, List

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Query.services import SavedQueryService


class TcSearchBasics:
    _cached_queries: Dict[str, BusinessObject] = None

    @classmethod
    def get_query_by_name(cls, query_name) -> Optional[BusinessObject]:     # returns: ImanQuery
        if cls._cached_queries is None:
            cls._cached_queries = dict()
            saved_queries_response = SavedQueryService.getSavedQueries()
            model_objs = saved_queries_response.serviceData.modelObjects
            for query in saved_queries_response.queries:
                cls._cached_queries[query.name] = model_objs[query.query.uid]
        return cls._cached_queries.get(query_name, None)

    @classmethod
    def exec_query(cls, query: BusinessObject, args: Dict[str, any], limit: int = 0) -> List[BusinessObject]:
        entries, values = [list(a) for a in zip(*args.items())] if args else [], []

        # get default params, and set them
        query_desc_resp = SavedQueryService.describeSavedQueries([query])
        for field in query_desc_resp.fieldLists[0].fields:
            if field.value and field.entryName not in entries:
                entries.append(field.entryName)
                values.append(field.value)

        exec_result = SavedQueryService.executeSavedQuery(
            query=query,
            entries=entries,
            values=values,
            limit=limit,
        )
        return exec_result.objects
