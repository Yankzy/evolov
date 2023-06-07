import graphene
from graphene_django.debug import DjangoDebug
from product.queries.ad_filters import adQueries
from users.query.auth import Authenticate
from users.query.company import CompanyQueries
from users.query.user_queries import UserQueries
from users.query.employee import EmployeeQueries
from users.mutation.user_mutations import UserMutations
from users.mutation.employee import EmployeeMutations
from users.mutation.follow import FollowMutations
from users.mutation.auth_mutations import Authorization
from product.queries.product_queries import ProductQueries
from product.mutations.product_mutations import ProductMutations
from product.mutations.resume import ResumeMutations
from payments.mutations import PaymentMutations
from product.queries.resume_filters import resumeQueries



class Query(
    Authenticate,
    ProductQueries,
    adQueries,
    CompanyQueries,
    EmployeeQueries,
    resumeQueries,
    UserQueries,
):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(
    UserMutations,
    FollowMutations,
    ProductMutations,
    PaymentMutations,
    Authorization,
    EmployeeMutations,
    ResumeMutations,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
