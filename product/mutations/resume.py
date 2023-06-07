from graphene import String, Mutation, ObjectType, Field
from graphql import GraphQLError
from observer import Notify
from observer.utils import create_update_resume, manage_category
from users.types import ResumeType, CategoryType, Facilities, Details, NearBy, SubCategoryType, AdType, Features, Benefits

klasses = {}

# def create_mutation(class_name_str, arguments, return_type, method):

#     class_vars = {
#         'to_return': return_type,
#         'Arguments': type('Meta', (object,), arguments),
#         'mutate': method,
#     }

#     pattern = r"([a-z]+)(?=[A-Z])"
#     replacement = lambda x: x.group(1).capitalize()
#     import re
#     klass_name = re.sub(pattern, replacement, class_name_str)
#     new_class = type(klass_name, (Mutation,), class_vars)
#     klasses[class_name_str] = new_class

#     return new_class


# def mutate_resume(self, info, **kwargs):
#     try:
#         created_object = Notify(
#             event_type=kwargs['event_type'], 
#             callback=create_update_resume, 
#             data=kwargs
#         ).subscribe()()
#         return resume(to_return=created_object.latest())
        
#     except Exception as e:
#         raise GraphQLError("An error occured") from e
    
def mutate_factory(callback, new_class):
    def mutate(self, info, **kwargs):
        try:
            created_object = Notify(
                event_type=kwargs['event_type'], 
                callback=callback, 
                data=kwargs
            ).subscribe()()
            return new_class(to_return=created_object.latest())
        except Exception as e:
            raise GraphQLError(e) from e
    return mutate

def create_mutation(**kwargs):
    class_vars = {
        'to_return': kwargs['return_type'],
        'Arguments': type('Meta', (object,), kwargs['arguments']),
        'mutate': mutate_factory(kwargs['callback'], 'new_class'),
    }

    pattern = r"([a-z]+)(?=[A-Z])" # convert snake_case to PascalCase
    replacement = lambda x: x.group(1).capitalize()
    import re
    klass_name = re.sub(pattern, replacement, kwargs['class_name_str'])
    new_class = type(klass_name, (Mutation,), class_vars)
    # set mutate attr of new_class
    setattr(new_class, 'mutate', mutate_factory(kwargs['callback'], new_class))


    klasses[kwargs['class_name_str']] = new_class

    return new_class

resume = create_mutation(
    class_name_str='create_resume',
    arguments={
        'user_id': String(required=True),
        'event_type': String(required=True),
    }, 
    return_type=Field(ResumeType), 
    callback=create_update_resume,
)

# def mutate_category(self, info, **kwargs):
#     try:
#         created_object = Notify(
#             event_type=kwargs['event_type'], 
#             callback=create_update_resume, 
#             data=kwargs
#         ).subscribe()()
#         return category(to_return=created_object.latest())
        
#     except Exception as e:
#         raise GraphQLError("An error occured") from e

# category = create_mutation(
#     'category',
#     {
#         'event_type': String(required=True),
#         'category_name': String(required=True),
#         'category_image_url': String(required=True),
#         'facilities': Facilities(),
#         'nearby': NearBy(),
#         'details': Details(),
#         'features': Features(),
#         'benefits': Benefits(),
#     },
#     Field(CategoryType),
#     mutate_category,
# )



class ResumeMutations(ObjectType):
    # for key, value in klasses.items():
        # key = value.Field()
        # locals()[key] = value
        # print(key, value)
    create_resume = resume.Field()
    # category = category.Field()
