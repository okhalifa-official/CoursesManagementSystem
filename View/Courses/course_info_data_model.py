text_box = "entry"
number = "number"
radio = "radio"
image = "img"
combo_box = "combo_box"
date = "date"

add_student_elements = [
    [{"Course Name*": text_box}],
    [{"Price*": number}],
    [{"Instructor*": combo_box}],
    [{"Start Date*": date}],
    [{"End Date*": date}]
]

add_student_elements_placeholders = {
    "Course Name*": "enter course name",
    "Price*": "e.g. 1000 EGP",
    "Instructor*": "select an instructor",
    "Start Date*": "select start date",
    "End Date*": "select end date"
}