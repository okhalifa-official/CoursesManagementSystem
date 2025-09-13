import random
import string
import fake_data as fake
def random_string(length=None):
    """Generate a random string of ASCII letters of random length between 4 and 20 if not specified."""
    if length is None:
        length = random.randint(4, 20)
    return ''.join(random.choices(string.ascii_letters, k=length))

Students = 'Students'
Courses = 'Courses'
Doctors = 'Doctors'
Student_Enrollment = 'Student_Enrollment'
Payments = 'Payments'

model = {
    'Students': ['id','Student', 'Course', 'Doctor', 'Payment ID'],
    'Courses': ['id', 'name', 'doctor_id'],
    'Doctors': ['id', 'name'],
    'Student_Enrollment': ['id', 'student_id', 'course_id'],
    'Payments': ['id', 'student_id', 'course_id']
}

# {Table_name: [{fk, to_table, pk},{..,..,..}]}
foreign_keys = {
    'Courses': [('doctor_id','Doctors','id')],
    'Student_Enrollment': [('student_id', 'Students', 'id'), ('course_id', 'Courses', 'id')],
    'Payments': [('student_id', 'Students', 'id'), ('course_id', 'Courses', 'id')]
}

# nullable_fields = {
#     'Courses': []
# }

from dataclasses import dataclass

@dataclass
class Student:
    entry = {}
    _student_fields = ['First Name*', 'Last Name*', 'Gender*', 
                       'E-mail', 'Country Code*', 'Phone Number*', 
                       'Address', 'University*', 'Barcode', 'Image']
    def generate_sample(self):
        for f in self._student_fields:
            self.entry[f] = random_string()
        self.entry['Gender*'] = 'Female'
        self.entry['Image'] = '/Users/omarkhalifa/Downloads/pfp.jpg'
    
    def load_fake_data(self):
        for i,f in enumerate(self._student_fields):
            match i:
                case 0:
                    val = random.choice(fake.names)
                case 1:
                    val = random.choice(fake.names)
                case 2:
                    val = random.choice(['Male', 'Female'])
                case 3:
                    val = fake.random_email(self.entry['First Name*'], self.entry['Last Name*'])
                case 4:
                    val = random.choice(fake.country_codes)
                case 5:
                    val = fake.random_phone()
                case 6:
                    val = random.choice(fake.addresses)
                case 7:
                    val = random.choice(fake.universities)
                case 8:
                    val = fake.random_barcode()
            self.entry[f] = val
            self.entry['Image'] = '/Users/omarkhalifa/Downloads/pfp.jpg'


@dataclass
class Course:
    entry = {}
    _course_fields = ['Course Name*', 'Price*', 'Instructor*', 
                       'Start Date*', 'End Date*']
    def generate_sample(self):
        for f in self._course_fields:
            self.entry[f] = random_string()
        self.entry['Instructor*'] = 'Dr. Green'
        self.entry['Image'] = '/Users/omarkhalifa/Downloads/pfp.jpg'
    
    def load_fake_data(self):
        strt, en = fake.random_start_end_dates()
        for i,f in enumerate(self._course_fields):
            match i:
                case 0:
                    val = fake.random_course_name()
                case 1:
                    val = fake.random_course_price()
                case 2:
                    val = 'Dr. Green'
                case 3:
                    val = strt
                case 4:
                    val = en
            self.entry[f] = val
            self.entry['Image'] = '/Users/omarkhalifa/Downloads/bigO.png'