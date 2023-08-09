from django.contrib import admin
from django.contrib.auth import models as auth_models

admin.site.register(auth_models.User)
