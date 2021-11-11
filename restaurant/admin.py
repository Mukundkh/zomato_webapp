from django.contrib import admin
from .models import restaurant_model, res_name
# Register your models here.
admin.site.register(restaurant_model)
admin.site.register(res_name)