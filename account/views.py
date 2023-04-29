from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Student, SubjectMarks
from django.db.models import Q




# Create your views here.
def index(request):
     return render(request, 'account/index.html')


def get_students(request):
    queryset = Student.objects.all()
    if request.GET.get('search'):
         search_item = request.GET.get('search')
         print(search_item)
         queryset = Student.objects.filter(
              Q(student_id__student_id__icontains=search_item) |
              Q(student_name__icontains=search_item) |              
              Q(department__department__icontains=search_item) |
              Q(student_email__icontains=search_item) |
              Q(student_address__icontains=search_item)
         )

    # contact_list = Contact.objects.all()
    paginator = Paginator(queryset, 20)  # Show 20 contacts per page.

    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)
    context = {'queryset':page_obj}
    # return render(request, "list.html", {"page_obj": page_obj})

    return render(request, 'account/getStudent.html',context)


def get_subject_marks(request,name):
     queryset = SubjectMarks.objects.filter(student=name)
     student_name = queryset[0].student.student_name
     student_id = queryset[0].student.student_id.student_id
     student_department = queryset[0].student.department.department
     context = {
          'queryset':queryset, 
          'student_name':student_name,
          'student_id':student_id,
          'student_department':student_department
          }
     return render(request,'account/subjectMarks.html',context)


def view_result(request):
     return render(request,'account/result.html')