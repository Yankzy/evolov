import graphene
from product.queries.filters_factory import FilterFactory
from product.models import Resume, Category
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType


class ResumeRelayNode(DjangoObjectType):
    class Meta:
        model = Resume
        interfaces = (graphene.relay.Node, )
    
    resume_id = graphene.Field(graphene.ID)

    def resolve_resume_id(self, info):
        return self.id


def create_query(categories):
    class RelayClass(graphene.ObjectType):
        one_resume = graphene.relay.Node.Field(ResumeRelayNode)


    for category_name, details in categories.items():
        field_name = f"{category_name}_filter"
        setattr(RelayClass, field_name, DjangoFilterConnectionField(
            ResumeRelayNode,
            filterset_class=FilterFactory(
                Resume,
                category_name,
                details
            )
        ))

    return RelayClass

resumeQueries = create_query({
    "resume_by_user": {'user':[['user', 'id', 'exact']]},
})

