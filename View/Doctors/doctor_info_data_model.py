text_box = "entry"
number = "number"
radio = "radio"
image = "img"

add_student_elements = [
    [{"First Name*": text_box}],[ {"Last Name*": text_box}],
    [{"Gender*": [radio, "Male", "Female"]}],
    [{"E-mail": text_box}],
    [{"Country Code*": number}],[{"Phone Number*": number}]
]

add_student_elements_placeholders = {
    "First Name*": "enter first name",
    "Last Name*": "enter last name",
    "E-mail": "enter e-mail address",
    "Country Code*": "enter country code",
    "Phone Number*": "enter phone number (whatsapp)"
}