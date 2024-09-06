from django.urls import path
from .views import *
urlpatterns = [
    path('',index, name='index'),
    path('students/',get_students, name='get-student'),
    path('marks/<str:id>',get_subject_marks, name='marks'),
    path('result/<str:name>', view_result, name='result'),
    path('department/', department_result , name='department-result'),
    path('download-pdf/<str:name>/', download_pdf, name='download_pdf'),
]