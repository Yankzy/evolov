import graphene
from product.models import Listing, SubCategory
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from graphene_django import DjangoObjectType
from django.db.models import Q




def FilterFactory( model_class, class_name, nested_key_qs):
    class_vars = {
        'min_price': django_filters.NumberFilter(
            method=lambda queryset, _, value: queryset.filter(details__price__gte=float(value))
        ),
       'max_price': django_filters.NumberFilter(
            method=lambda queryset, _, value: queryset.filter(details__price__lte=float(value))
        ),
        'Meta': type( 'Meta', (object, ), {
            "model": model_class,
            "fields": {
                'sub_category__sub_category_name': ['contains'],
                'status': ['contains'],
            }
        })
    }


    def numeric_filter(queryset, name, value):
        return queryset.filter(**{f'details__{name}__gte': float(value)})
    
    for key in list(nested_key_qs.keys()):
        for item in nested_key_qs[key]:
            if item[1] == 'string':
                class_vars[item[0]] = django_filters.CharFilter(
                    field_name=f'{key}__{item[0]}', 
                    lookup_expr=item[2],
                )
                
            elif item[1] == 'bool':
                class_vars[item[0]] = django_filters.BooleanFilter(
                    field_name=f'{key}__{item[0]}', 
                    lookup_expr=item[2],
                )

            elif item[1] == 'number':
                class_vars[item[0]] = django_filters.NumberFilter(method=numeric_filter)

    return type( class_name, (django_filters.FilterSet, ), class_vars )


class ListingNode(DjangoObjectType):
    class Meta:
        model = Listing
        interfaces = (graphene.relay.Node, )


class ListingQuery(graphene.ObjectType):
    one_listing = graphene.relay.Node.Field(ListingNode)
    all_listings = DjangoFilterConnectionField(
        ListingNode, 
        filterset_class=FilterFactory(  
            Listing, 
            'ListingFilter',
            SubCategory.objects.filter(sub_category_name='real_estate').values('details', 'facilities', 'nearby')[0]
        ),
    )


