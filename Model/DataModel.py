from Model import DataArchitecture as DataArch
from Query import select
import DB

model = {}
for i in range(3):
    model[DataArch.entities[i]] = DataArch.columns[i]

from dataclasses import dataclass


def get_image_path(f_name, l_name, phone):
    return f_name + l_name + phone[-5:]


@dataclass
class Student:
    entry = {}
    _student_columns = DataArch.columns[0]
    _student_data = {}
    _student_fields = ['First Name*', 'Last Name*', 'Gender*', 
                       'E-mail', 'Country Code*', 'Phone Number*', 
                       'Address', 'University*', 'Barcode', 'Image']
    
    def __init__(self, id):
        # load student data with given 'ID'
        record = select.select_by_id(DB.db(), 'students', id).fetchall()[0]
        if len(record) < 1:
            return False
        for i in range(len(self._student_columns)):
            self._student_data[self._student_columns[i]] = record[i]

        self._student_data['Image'] = get_image_path(self._student_data['First Name'], self._student_data['Last Name'], self._student_data['Phone Number'])


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
        if len(record) < 1:
            return False
        for i in range(len(self._course_columns)):
            self._course_data[self._course_columns[i]] = record[i]
    

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
        if len(record) < 1:
            return False
        for i in range(len(self._doctor_columns)):
            self._doctor_data[self._doctor_columns[i]] = record[i]

Students = []
Doctors = []
Courses = []