from django.contrib import admin
from .models import Company, Employee, UserAuthToken, User

admin.site.register(UserAuthToken)
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(User)
