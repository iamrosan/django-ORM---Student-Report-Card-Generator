

def generate_student_division(percentage:float)->str:
    if percentage>80:
          return 'Distinction'
    elif percentage>70:
        return 'First'
    elif percentage>60:
        return 'Second'
    elif percentage>50:
        return 'Third'
    else:
        return 'Fail'
    