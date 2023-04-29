from django.urls import path
from .views import *
urlpatterns = [
    path('',index, name='index'),
    path('students/',get_students, name='get-student'),
    path('marks/<str:name>',get_subject_marks, name='marks'),
]