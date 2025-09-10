text_box = "entry"
number = "number"
radio = "radio"
image = "img"

add_student_elements = [
    [{"First Name*": text_box}],[ {"Last Name*": text_box}],
    [{"Gender*": [radio, "Male", "Female"]}],
    [{"E-mail": text_box}],
    [{"Country Code*": number}],[{"Phone Number*": number}],
    [{"Address": text_box}],[{"University*": text_box}],
    [{"Barcode": number}]
]

add_student_elements_placeholders = {
    "First Name*": "enter first name",
    "Last Name*": "enter last name",
    "E-mail": "enter e-mail address",
    "Country Code*": "enter country code",
    "Phone Number*": "enter phone number (whatsapp)",
    "Address": "e.g. 27th baker st. , California",
    "University*": "enter university name",
    "Barcode": "enter(scan) barcode" 
}