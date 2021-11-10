from django.urls import path
from . import views

urlpatterns = [
    path("", views.index,name="restaurant"),
    path("<int:id>", views.restaurant_detail, name="detail_restaurant"),
    
]
