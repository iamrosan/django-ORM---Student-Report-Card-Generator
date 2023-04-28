from faker import Faker 
fake = Faker()
from .models import Department, StudentID, Student, Subject, SubjectMarks
import random



def seed_db(n=48) -> None:
    department_objs = Department.objects.all()
    try:

        for j in range(len(department_objs)-1): 
            for i in range(n):
                # department_index = random.randint(0, len(department_objs)-1)
                # department = department_objs[department_index]
                department = department_objs[j] #Code refactor
                student_id = f'KCE075{str(department_objs[j].department[:3].upper())}0{i+1}'
                student_name = fake.name()
                student_email = fake.email()
                student_age = random.randint(18,25)
                student_address = fake.address()

                studentID_data = StudentID.objects.create(student_id=student_id)

                student_data = Student.objects.create(
                                                        department=department,
                                                        student_id = studentID_data,
                                                        student_name = student_name,
                                                        student_age= student_age,
                                                        student_address =student_address,
                                                        student_email = student_email
                                                    )
    except Exception as e :
        print(f"ERROR OCCURED :: {e}")


def create_subject_marks():
    try:
        student_obj = Student.objects.all()
        for std in student_obj:
            subjects_obj = Subject.objects.all()
            for sub in subjects_obj:
                SubjectMarks.objects.create(
                    student = std,
                    subject = sub,
                    marks = random.randint(0, 100)
                )
    
    except Exception as e:
        print(f'Error :: {e}')