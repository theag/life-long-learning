from django.urls import path

from . import views

app_name = "members"

urlpatterns = [
    path('', views.index, name='index'),
    path('members/add', views.add, name="add"),
    path('members/<int:member_id>', views.edit, name="edit"),
    path('courses',views.courses, name='courses'),
    path('courses/add', views.add_course, name="add_course"),
    path('courses/<int:course_id>', views.edit_course, name="edit_course"),
]