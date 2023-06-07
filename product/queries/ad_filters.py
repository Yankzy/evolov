import graphene
from product.queries.filters_factory import FilterFactory
from product.models import Ad, Category
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from graphql import GraphQLError


class AdRelayNode(DjangoObjectType):
    class Meta:
        model = Ad
        interfaces = (graphene.relay.Node, )

    ad_id = graphene.Field(graphene.ID)

    # this annotation adds the id field to the AdRelayNode
    def resolve_ad_id(self, info):
        return self.id

    

    


def create_query(categories):
    class RelayClass(graphene.ObjectType):
        one_ad = graphene.relay.Node.Field(AdRelayNode)


    for category_name, details in categories.items():
        field_name = f"{category_name}_filter"
        setattr(RelayClass, field_name, DjangoFilterConnectionField(
            AdRelayNode,
            filterset_class=FilterFactory(
                Ad,
                category_name,
                details
            )
        ))

    return RelayClass




adQueries = create_query({
    "vehicle": list(Category.objects.filter(category_name='vehicle').values('details'))[0],
    "vacancy": list(Category.objects.filter(category_name='vacancy').values('details'))[0],
    # "ads_by_user": {'user':[['user', 'id', 'exact']]},
    # "ads_by_company": {'user':[['user', 'id', 'exact']]},
    # "ads_by_employee": {'user':[['user', 'id', 'exact']]},
})

