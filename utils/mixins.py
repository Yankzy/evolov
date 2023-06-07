import graphene


class PaginatedTypeMixin(graphene.ObjectType):
    """
    base pagination object type
    - childs should override the objects fields
    """
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = None
    total_objects = graphene.Int()
