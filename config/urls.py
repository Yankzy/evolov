
from django.urls import path, include
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.contrib import admin
from django.contrib.auth.mixins import LoginRequiredMixin


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG))),
    path('payments/', include('payments.urls')),
]
# http://127.0.0.1:8080/payments/stripe-webhook