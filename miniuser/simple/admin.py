from django.contrib import admin

from simple import models as simple_models

admin.site.register(simple_models.Issue)
admin.site.register(simple_models.MyUser)
