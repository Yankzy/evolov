from graphene import String, Mutation, List, ObjectType, Boolean
from observer.utils import manage_category, manage_sub_category, create_update_ad, create_update_resume
from product.models import Category, SubCategory, Ad, Resume
from users.types import CategoryType, Facilities, Details, NearBy, SubCategoryType, AdType, Features, Benefits, ResumeType, UserType
from observer import Notify
from graphql import GraphQLError
import graphene
from users.models import Employee, Activity, User
from utils.permissions import IsAuthenticated, permission_checker, InstancePermission
from graphene.types.generic import GenericScalar
from users.models import User


class CategoryMutation(Mutation):
    to_return = graphene.List(CategoryType)

    class Arguments:
        event_type = String(required=True)
        category_name = String(required=True) 
        category_image_url = String(required=True) 
        facilities = Facilities()
        nearby = NearBy()
        details = Details()
        features = Features()
        benefits = Benefits()

    # @permission_checker([IsAuthenticated])
    def mutate(self, info, **kwargs):
        if kwargs.get('event_type') not in ['create_category', 'delete_category', 'update_category']:
            raise GraphQLError("Wrong event_type")

        Notify(
            event_type=kwargs['event_type'], 
            callback=manage_category, 
            data=kwargs
        ).subscribe()()

        return CategoryMutation(to_return=Category.objects.filter(category_name=kwargs['category_name']))


class SubCategoryMutation(Mutation):
    to_return = graphene.List(SubCategoryType)

    class Arguments:
        event_type = String(required=True)
        category_name = String(required=True) 
        sub_category_name = String(required=True) 
        sub_category_image_url = String(required=True)

    # @permission_checker([IsAuthenticated])
    def mutate(self, info, **kwargs):
        if kwargs.get('event_type') not in ['create_sub_category', 'delete_sub_category', 'update_sub_category']:
            raise GraphQLError("Wrong event_type")

        Notify(
            event_type=kwargs['event_type'], 
            callback=manage_sub_category, 
            data=kwargs
        ).subscribe()()

        return SubCategoryMutation(to_return=SubCategory.objects.filter(sub_category_name=kwargs["sub_category_name"]))


class CreateAd(Mutation):
    to_return = graphene.Field(AdType)

    class Arguments:
        event_type = String(required=True)
        sub_category_name = String(required=True) 
        details = Details()
        facilities = Facilities()
        nearby = NearBy()
        features = Features()
        benefits = Benefits()
        gallery = GenericScalar()

    @permission_checker([IsAuthenticated])
    def mutate(self, info, **kwargs):

        kwargs['user'] = info.context.user
        if kwargs.get('event_type') not in ["create_ad", "update_ad"]:
            raise GraphQLError("Wrong event_type")

        ad = Notify(
            event_type=kwargs['event_type'], 
            callback=create_update_ad, 
            data=kwargs
        ).subscribe()()

        return CreateAd(to_return=ad)



class ResumeMutation(Mutation):
    to_return = graphene.Field(ResumeType)

    class Arguments:
        event_type = String(required=True)
        personal_information = GenericScalar() 
        work_experience = GenericScalar() 
        skills = GenericScalar() 
        languages = GenericScalar() 
        education = GenericScalar()
        documents = GenericScalar()

    # @permission_checker([IsAuthenticated])
    def mutate(self, info, **kwargs):

        kwargs['user'] = User.objects.get(email='evolov@gmail.com')
        # kwargs['user'] = info.context.user
        if kwargs.get('event_type') not in ["create_resume", "update_resume"]:
            raise GraphQLError("Wrong event_type")

        resume = Notify(
            event_type=kwargs['event_type'], 
            callback=create_update_resume, 
            data=kwargs
        ).subscribe()()

        return ResumeMutation(to_return=resume)


class UpdateAd(Mutation):
    to_return = graphene.Field(AdType)

    class Arguments:
        email = String(required=True)
        uid = String(required=True)
        ad_id = String(required=True)
        event_type = String(required=True)
        status = String() 
        is_active = Boolean() 
        facilities = Facilities()
        nearby = NearBy()
        details = Details()
        gallery = GenericScalar()
    
    def mutate(self, info, **kwargs):
        if kwargs.get('event_type') != "update_ad":
            raise GraphQLError("Wrong event_type")

        trigger = Notify(event_type=kwargs["event_type"], callback=create_update_ad).subscribe()
        trigger(kwargs["event_type"], kwargs)

        # ad = Ad.objects.filter(user="")
        return UpdateAd(to_return=Ad.objects.all())


class PublishADByCompany(Mutation):
    to_return = graphene.Field(AdType)

    class Arguments:
        employees_id = graphene.List(graphene.ID)
        sub_category_id = graphene.ID(required=True)
        facilities = graphene.JSONString()
        near_by = graphene.JSONString()
        details = graphene.JSONString()


    # @permission_checker([IsCompany, CanPostAD])
    def mutate(self, info, **kwargs):
        company = info.context.user.company

        users = [company.user]

        if kwargs.get('employees_id') is not None:
            for employee_id in kwargs.pop('employees_id'):
                try:
                    employee = Employee.objects.get(id=employee_id)
                except Employee.DoesNotExist as e:
                    raise GraphQLError("one or more employee id not valid") from e
                
                if employee.company != company:
                    raise GraphQLError("one or more employees does not belong to the company")
                
                users.append(employee.user)
        
        ad = Ad(**kwargs)
        ad.save()

        for user in users:
            ad.user.add(user)

        return PublishADByCompany(ad)



class PublishAdByEmployee(Mutation):
    to_return = graphene.Field(AdType)

    class Arguments:
        sub_category_id = graphene.ID(required=True)
        employees_id = graphene.List(graphene.ID)
        facilities = graphene.JSONString()
        near_by = graphene.JSONString()
        details = graphene.JSONString()

    # @permission_checker([IsEmployee])
    def mutate(self, info, **kwargs):
        user = info.context.user

        company = user.employee.company

        users = {user, company.user}

        if kwargs.get('employees_id') is not None:
            for employee_id in kwargs.pop('employees_id'):
                try:
                    emp = Employee.objects.get(pk=employee_id)
                    
                    if emp.company != company:
                        raise GraphQLError("one or more employees are not part of the current company")
                    
                    users.add(emp.user)
                except Employee.DoesNotExist:
                    raise GraphQLError("Employee does not exist")
        ad = Ad(**kwargs)
        ad.save()

        for user in users:
            ad.user.add(user)

        return PublishAdByEmployee(ad)


class UpdateAdStatus(Mutation):
    to_return = graphene.Field(AdType)

    class Arguments:
        ad_id = graphene.ID(required=True)
        status = graphene.String(required=True)

    @permission_checker([IsAuthenticated])
    def mutate(self, info, **kwargs):
        print(kwargs['status'])
        user = info.context.user
        if kwargs.get('status') not in ['ACTIVE', 'DELETED', 'SOLD', 'REVIEW', 'UNPUBLISHED']:
            raise GraphQLError("Wrong status")

        try:
            ad = Ad.objects.get(id=kwargs['ad_id'], user=user)
            ad.status = kwargs['status']
            ad.save()
        except Ad.DoesNotExist as e:
            raise GraphQLError("ad object does not exist") from e

        return UpdateAdStatus(ad)


class DeleteAD(Mutation):
    to_return = graphene.Boolean()

    class Arguments:
        ad_id = String(required=True)

    # @permission_checker([IsAuthenticated])
    def mutate(self, info, **kwargs):
        try:
            ad = Ad.objects.get(pk=kwargs['ad_id'])
            InstancePermission.check_instance_owner(ad, info.context.user)
            ad.delete()
            return True
        except Ad.DoesNotExist as e:
            raise GraphQLError("Object Not Found") from e


class ApplyMutation(graphene.Mutation):
    class Arguments:
        vacancy_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)

    success = graphene.Boolean()
    vacancy = graphene.Field(AdType)

    def mutate(self, info, vacancy_id, user_id):
        vacancy = Ad.objects.get(pk=vacancy_id)
        resume = Resume.objects.get(user__id=user_id)

        if 'applications' not in vacancy.details:
            vacancy.details['applications'] = []

        if str(resume.id) not in vacancy.details['applications']:
            vacancy.details['applications'].append(str(resume.id))
            vacancy.save()

        return ApplyMutation(success=True, vacancy=vacancy)
    

class StatisticMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)
        statistic = graphene.String(required=True)
        is_like = graphene.Boolean(required=True)

    to_return = graphene.Field(AdType)
    error = graphene.String()

    def mutate(self, info, id, user_id, statistic, is_like):
        if statistic not in ["likes", "reviews", "views", "shares"]:
            raise GraphQLError("Wrong event_type")
        try:
            ad = Ad.objects.get(id=id)
            if 'liked_users' not in ad.statistics:
                ad.statistics['liked_users'] = []
                
                
            if statistic == "likes":
                from django.contrib.contenttypes.models import ContentType
                if is_like:
                    if user_id not in ad.statistics['liked_users']:
                        ad.statistics['liked_users'].append(user_id)
                        ad.statistics['likes'] += 1
                        activity = Activity(content_object=ad, activity_type='LIKE', user=User.objects.get(id=user_id))
                        activity.save()
                else:
                    if user_id in ad.statistics['liked_users']:
                        ad.statistics['liked_users'].remove(user_id)
                        ad.statistics['likes'] -= 1
                        Activity.objects.filter(activity_type='LIKE').delete()
                        
            else: ad.statistics[statistic] += 1
            ad.save()
        except Ad.DoesNotExist:
            return StatisticMutation(to_return=None, error=f"Ad with id {id} does not exist")
        except KeyError:
            return StatisticMutation(to_return=None, error=f"{statistic} is not a valid statistic")

        return StatisticMutation(to_return=ad)


class ProductMutations(ObjectType):
    category = CategoryMutation.Field()
    sub_category = SubCategoryMutation.Field()
    publish_ad_by_company = PublishADByCompany.Field()
    publish_ad_by_employee = PublishAdByEmployee.Field()
    create_ad = CreateAd.Field()
    delete_ad = DeleteAD.Field()
    update_ad = UpdateAd.Field()
    update_ad_status = UpdateAdStatus.Field()
    resume = ResumeMutation.Field()
    apply_for_vacancy = ApplyMutation.Field()
    statistics = StatisticMutation.Field()
