from django.urls import path

from . import views

app_name = "members"

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name="add"),
    path('<int:member_id>', views.edit, name="edit"),
]