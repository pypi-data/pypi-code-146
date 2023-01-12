
from model_search import model_search

from delivery.models import Warehouse, City, DeliveryMethod


def search_warehouses(delivery_method_id, city, query, limit=None):

    if not query or not city or not delivery_method_id:
        return []

    try:
        city = city.split(' - ')[0]
    except Exception:
        return []

    try:
        delivery_method = DeliveryMethod.objects.get(id=delivery_method_id)
    except DeliveryMethod.DoesNotExist:
        return []

    warehouses = Warehouse.objects.filter(
        delivery_method__code=delivery_method.code,
        city__name=city
    )

    queryset = model_search(query, warehouses, ['name'])

    if limit is not None:
        return queryset[:limit]

    return queryset


def search_cities(query, limit=10):

    if not query:
        return []
    
    items = list(
        City.objects.filter(name__istartswith=query).order_by("name")[:limit]
    )
    
    if len(items) < limit:
        items += list(
            model_search(
                query, 
                City.objects.exclude(id__in=[i.id for i in items]),
                ['name']
            )
        )
    
    return items[:limit]
