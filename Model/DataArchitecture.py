entities = ['students', 'doctors','courses', 'studentcourse', 'payments']

columns = [
    # students
    [
        "ID",
        "First Name",
        "Last Name",
        "Gender",
        "Country Code",
        "Phone Number",
        "Address",
        "Email",
        "University",
        "Barcode"
    ],
    # doctors
    [
        "ID",
        "First Name",
        "Last Name",
        "Gender",
        "Email",
        "Country Code",
        "Phone Number"
    ],
    # courses
    [
        "ID",
        "Course Name",
        "Doctor Name",
        "Price",
        "Start Date",
        "End Date"
    ],
    # student_course
    [
        "ID",
        "Student ID",
        "Doctor ID",
        "Course Name",
        "Course Price",
        "Course Start Date",
        "Course End Date",
        "Enrollment Date",
        "Course ID"
    ],
    # payments
    [
        "ID",
        "Student ID",
        "Student Course ID",
        "Payment Date",
        "Amount Paid"
    ]
]


text_box = "entry"
number = "number"
radio = "radio"
image = "img"
combo_box = "combo_box"
date = "date"

add_student_elements = [
    [{columns[0][1]: text_box}],[ {columns[0][2]: text_box}],
    [{columns[0][3]: [radio, "Male", "Female"]}],
    [{columns[0][4]: number}],[{columns[0][5]: number}],
    [{columns[0][6]: text_box}], [{columns[0][7]: text_box}],
    [{columns[0][8]: text_box}],
    [{columns[0][9]: number}]
]

add_student_elements_placeholders = {
    columns[0][1]: "enter first name",
    columns[0][2]: "enter last name",
    columns[0][4]: "enter country code",
    columns[0][5]: "enter phone number (whatsapp)",
    columns[0][6]: "e.g. 27th baker st. , California",
    columns[0][7]: "enter e-mail address",
    columns[0][8]: "enter university name",
    columns[0][9]: "enter(scan) barcode" 
}

add_doctor_elements = [
    [{columns[1][1]: text_box}],[ {columns[1][2]: text_box}],
    [{columns[1][3]: [radio, "Male", "Female"]}],
    [{columns[1][4]: text_box}],
    [{columns[1][5]: number}],[{columns[1][6]: number}]
]

add_doctor_elements_placeholders = {
    columns[1][1]: "enter first name",
    columns[1][2]: "enter last name",
    columns[1][4]: "enter e-mail address",
    columns[1][5]: "enter country code",
    columns[1][6]: "enter phone number (whatsapp)"
}

add_course_elements = [
    [{columns[2][1]: text_box}],
    [{columns[2][2]: combo_box}],
    [{columns[2][3]: number}],
    [{columns[2][4]: date}],
    [{columns[2][5]: date}]
]

add_course_elements_placeholders = {
    columns[2][1]: "enter course name",
    columns[2][2]: "select an instructor",
    columns[2][3]: "e.g. 1000 EGP",
    columns[2][4]: "select start date",
    columns[2][5]: "select end date"
}