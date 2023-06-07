import graphene


class Output:
    """
    A class to all public classes extend to
    padronize the output
    """
    error = graphene.String(default_value=None)
    status = graphene.Boolean(default_value=True)
