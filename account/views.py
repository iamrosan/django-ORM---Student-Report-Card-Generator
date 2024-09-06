from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Student, SubjectMarks
from django.db.models import Q, Sum

# pdf import
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Utils import
from .utils import generate_student_division

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


def get_subject_marks(request,id):
     queryset = SubjectMarks.objects.filter(student=id)
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

def view_result(request, name):
    # Retrieve the student's marks and related details
    queryset = SubjectMarks.objects.filter(student__student_name__icontains=name)
    
    if not queryset.exists():
        return HttpResponse("No data found for this student.")
    
    # Get student details
    student_name = queryset[0].student.student_name
    student_id = queryset[0].student.student_id.student_id
    student_department = queryset[0].student.department.department
    
    # Calculate total marks and percentage for the student
    total = queryset.aggregate(total=Sum('marks'))['total']
    percentage = round(float(total) / 9, 2)  # Assuming 9 subjects or change as needed
    
    # Division logic (assuming a separate function exists)
    division = generate_student_division(percentage)
    
    # Fetch total marks of all students
    all_students_total = (
        SubjectMarks.objects.values('student__student_name')
        .annotate(total_marks=Sum('marks'))
        .order_by('-total_marks')  # Order by total marks descending
    )
    
    # Calculate the student's rank
    rank = 1
    for i, student in enumerate(all_students_total, 1):
        if student['student__student_name'] == student_name:
            rank = i
            break
    
    # Prepare the context for rendering the template
    context = {
        'student_name': student_name,
        'student_id': student_id,
        'student_department': student_department,
        'result': {
            'total': total,
            'percentage': percentage,
            'rank': rank,
            'division': division,
        },
        'queryset': queryset,  # Pass the student's subject marks for display
    }
    
    return render(request, 'account/result.html', context)

def department_result(request):
     pass


def download_pdf(request, name):
    try:
        queryset = SubjectMarks.objects.filter(student__student_name__icontains=name)
        if not queryset.exists():
            return HttpResponse("No data found for this student.")

        student_name = queryset[0].student.student_name
        student_id = queryset[0].student.student_id.student_id
        student_department = queryset[0].student.department.department
        total = queryset.aggregate(total=Sum('marks'))
        percentage = round(float(total['total']) / 9, 2)
        rank = 1  # Calculate the rank based on your logic
        division = generate_student_division(percentage)

        context = {
            'student_name': student_name,
            'student_id': student_id,
            'student_department': student_department,
            'result': {
                'total': total,
                'percentage': percentage,
                'rank': rank,
                'division': division,
            },
            'queryset': queryset,  # Add queryset to context
        }

        template_path = 'account/result_pdf.html'
        template = get_template(template_path)
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        # Generate PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse(f'We had some errors <pre>{html}</pre>')

        return response

    except Exception as e:
        return HttpResponse(f"Error occurred: {e}")