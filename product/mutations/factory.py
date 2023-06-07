import graphene
from graphene import String
from utils.permissions import InstancePermission
from graphql import GraphQLError
from product.models import Category, SubCategory, Ad



class MutationFactory:
    def create_mutation(self, class_name, arguments, return_type, method_content):
        class_vars = {
            'to_return': return_type,
            'Arguments': type('Meta', (object,), dict(arguments.items())),
        }

        # Define the mutate method using exec
        exec(f"def mutate(self, info, **kwargs):\n{method_content}", locals())


        return type( class_name, (object, ), class_vars)


method_content = """
    try:
        ad = Ad.objects.get(pk=kwargs['ad_id'])
        InstancePermission.check_instance_owner(ad, info.context.user)
        ad.delete()
        return True
    except Ad.DoesNotExist as e:
        raise GraphQLError("Object Not Found") from e
"""


# Example usage
factory = MutationFactory()
arguments = {
    'ad_id': String(required=True),
    'status': String(required=True)
}
return_type = graphene.Boolean()
CreatedClass = factory.create_mutation(arguments, return_type, method_content)
