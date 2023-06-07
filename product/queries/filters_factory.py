import django_filters
from django_filters.rest_framework import BaseInFilter, CharFilter
from django.db.models import Q
from graphql import GraphQLError



def q_filter(q_objects, queryset):
    # Combine the Q objects using the | operator
    q = q_objects[0]
    for i in range(1, len(q_objects)):
        q |= q_objects[i]
    # Filter the queryset using the combined Q object
    return queryset.filter(q)

def bool_filter(queryset, name, value):
    if value:
        # Create a Q object for each item in value
        q_objects = [Q(**{f'{name}__{item}': True}) for item in value]
        return q_filter(q_objects, queryset)
    return queryset


def string_filter(queryset, name, value):
    if value:
        # Create a Q object for each item in value
        q_objects = [Q(**{f'{name}__icontains': item}) for item in value]
        return q_filter(q_objects, queryset)
    return queryset


def range_filter(queryset, name, value):
    if value:
        return queryset.filter(**{f"{name}__range": [float(value[0]), float(value[1])]})
    return queryset


def user_filter(queryset, _, value):
    if queryset.model.__name__ == 'User':
        return queryset.filter(id=value) if value else {}
    else:
        return queryset.filter(user__id=value) if value else {}
    
    

    
def FilterFactory( model_class, class_name, nested_key_qs):
    class_vars = {
        'Meta': type( 'Meta', (object, ), {
            "model": model_class,
        }),
    }
    if model_class.__name__ == 'Resume':
        class_vars['Meta'].fields = {
            'status': ['icontains'],
        }
    elif model_class.__name__ == 'Ad':
        class_vars['Meta'].fields = {
            'sub_category__sub_category_name': ['icontains'], 
            'is_active': ['exact']
        }
    elif model_class.__name__ == 'User':
        class_vars['Meta'].fields = {
            'is_active': ['exact']
        }

    if nested_key_qs:
        for key in nested_key_qs:
            for item in nested_key_qs[key]:
                if item[1] == 'string':
                    class_vars[item[0]] = BaseInFilter(
                        field_name=f'{key}__{item[0]}', 
                        method=string_filter
                    )
                    
                elif item[1] == 'bool':
                    class_vars[item[0]] = BaseInFilter(
                        field_name=f'{item[0]}', 
                        method=bool_filter
                    )

                elif item[1] == 'number':
                    class_vars[item[0]] = BaseInFilter(
                        field_name=f'{key}__{item[0]}', 
                        method=range_filter
                    )

                elif item[1] == 'id':
                    class_vars[item[0]] = CharFilter(
                        field_name=item[0], 
                        method=user_filter
                    )

    return type( class_name, (django_filters.FilterSet, ), class_vars)

