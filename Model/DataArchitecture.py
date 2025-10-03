entities = ['students', 'doctors','courses', 'studentcourse', 'payments']

columns = [
    # students
    [
        "id",
        "first_name",
        "last_name",
        "gender",
        "country_code",
        "phone_number",
        "address",
        "email",
        "university",
        "barcode"
    ],
    # doctors
    [
        "id",
        "first_name",
        "last_name",
        "gender",
        "email",
        "country_code",
        "phone_number"
    ],
    # courses
    [
        "id",
        "name",
        "doctor_name",
        "price",
        "start_date",
        "end_date"
    ],
    # student_course
    [
        "id",
        "student_id",
        "doctor_id",
        "course_name",
        "course_price",
        "course_start_date",
        "course_end_date",
        "enrollment_date",
        "course_id"
    ],
    # payments
    [
        "id",
        "student_id",
        "student_course_id",
        "payment_date",
        "amount_paid"
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