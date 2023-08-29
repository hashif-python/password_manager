from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(UserPassword)
admin.site.register(SharePassword)
admin.site.register(PasswordEditRequests)
admin.site.register(Organisation)