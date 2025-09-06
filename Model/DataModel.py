model = {
    'Students': ['id', 'name'],
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