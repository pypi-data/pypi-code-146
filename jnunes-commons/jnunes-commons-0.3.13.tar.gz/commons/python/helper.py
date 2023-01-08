from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_pagination(request, object_list, per_page):
    paginator = Paginator(object_list=object_list, per_page=per_page)
    page = request.GET.get('page')
    try:
        elements = paginator.page(page)
    except PageNotAnInteger:
        elements = paginator.page(1)
    except EmptyPage:
        elements = paginator.page(paginator.num_pages)
    return elements


def is_ajax(request) -> bool:
    try:
        return request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    except Exception as e:
        raise RuntimeError(e)


def is_delete_method(request) -> bool:
    try:
        return request.method == 'DELETE'
    except Exception as e:
        raise RuntimeError(e)


def is_post_method(request) -> bool:
    try:
        return request.method == 'POST'
    except Exception:
        raise RuntimeError
