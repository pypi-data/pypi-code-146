from django.db.models import Count
from django.db.models import F
from django.db.models import OuterRef
from django.db.models import Subquery
from django.db.models import Sum
from django.db.models.functions import Coalesce


def get_products_query_set(qs):
    qs = qs.prefetch_related('all_skins')
    filterd = qs.filter(pk=OuterRef('pk'))
    skin_count = filterd.annotate(skin_count=Count('all_skins'))
    skin_score = filterd.annotate(skin_score=Coalesce(Sum('all_skins__value'), 0))
    qs = qs.annotate(
        skin_count=Subquery(skin_count.values('skin_count')),
        skin_score=Subquery(skin_score.values('skin_score')),
    )
    return qs
