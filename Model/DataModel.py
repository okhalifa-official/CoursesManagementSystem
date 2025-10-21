import random
import string
from Model import DataArchitecture as DataArch
from Query import select
import DB
def random_string(length=None):
    """Generate a random string of ASCII letters of random length between 4 and 20 if not specified."""
    if length is None:
        length = random.randint(4, 20)
    return ''.join(random.choices(string.ascii_letters, k=length))


model = {}
for i in range(3):
    model[DataArch.entities[i]] = DataArch.columns[i]


from dataclasses import dataclass

@dataclass
class Student:
    entry = {}
    _student_columns = DataArch.columns[0]
    _student_data = {'Image':None}
    _student_fields = ['First Name*', 'Last Name*', 'Gender*', 
                       'E-mail', 'Country Code*', 'Phone Number*', 
                       'Address', 'University*', 'Barcode', 'Image']
    
    def __init__(self, id):
        # load student data with given 'ID'
        record = select.select_by_id(DB.db(), 'students', id).fetchall()[0]
        for i in range(len(self._student_columns)):
            self._student_data[self._student_columns[i]] = record[i]

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
    _course_columns = DataArch.columns[2]
    _course_data = {'Image':None}
    _course_fields = ['Course Name*', 'Price*', 'Instructor*', 
                       'Start Date*', 'End Date*', 'Image']
    
    def __init__(self, id):
        # load course data with given 'ID'
        record = select.select_by_id(DB.db(), 'courses', id).fetchall()[0]
        for i in range(len(self._course_columns)):
            self._course_data[self._course_columns[i]] = record[i]
    
    def generate_sample(self):
        for f in self._course_fields:
            self.entry[f] = random_string()
        self.entry['Instructor*'] = 'Dr. Yousef Ahmed'
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
                    val = 'Dr. Yousef Mohamed'
                case 3:
                    val = strt
                case 4:
                    val = en
            self.entry[f] = val
            self.entry['Image'] = '/Users/omarkhalifa/Downloads/medical.jpeg'

@dataclass
class Doctor:
    entry = {}
    _doctor_columns = DataArch.columns[1]
    _doctor_data = {}
    _doctor_fields = ['First Name*', 'Last Name*', 'Gender*', 
                       'E-mail', 'Country Code*', 'Phone Number*']
    
    def __init__(self, id):
        # load student data with given 'ID'
        record = select.select_by_id(DB.db(), 'doctors', id).fetchall()[0]
        for i in range(len(self._doctor_columns)):
            self._doctor_data[self._doctor_columns[i]] = record[i]
    
    def generate_sample(self):
        for f in self._doctor_fields:
            self.entry[f] = random_string()
        self.entry['Gender*'] = 'Female'
    
    def load_fake_data(self):
        for i,f in enumerate(self._doctor_fields):
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
            self.entry[f] = val

Students = []
Doctors = []
Courses = []