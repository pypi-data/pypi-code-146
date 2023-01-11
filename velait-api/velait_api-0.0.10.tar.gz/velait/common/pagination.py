
def get_page_limits(page: int, page_size: int):
    offset = page * page_size
    return offset, offset + page_size


__all__ = ['get_page_limits']
