from django.core.paginator import Paginator
from typing import Iterable

def common_pagination(objects: Iterable, page=1, per_page=25) -> dict:
    """
    custom paginator for paginated object types

    Args:
        objects (Iterable): list of ordered objects to be paginated
        page (int, optional): page of the paginator object. Defaults to 1.
        per_page (int, optional): number of objects to be inserted on a single page. Defaults to 25.

    Returns:
        dict: a compatible maping for the utils.mixins.PaginatedTypeMixin type
    """
    paginator = Paginator(objects, per_page)

    result = paginator.page(page)  # results from the current page

    return {
        'page': page,
        'pages': paginator.num_pages,
        'has_next': result.has_next(),
        'has_prev': result.has_previous(),
        'objects': result.object_list,
        'total_objects': objects.count(),
    }