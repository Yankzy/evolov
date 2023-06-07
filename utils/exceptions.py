# from graphql.error import GraphQLError
from graphql.error import GraphQLError, GraphQLLocatedError



class PermissionDenied(Exception):
    def __init__(self, message = None, status_code=400):
        if message is None:
            message = "Permission Denied"

        super().__init__(message)
