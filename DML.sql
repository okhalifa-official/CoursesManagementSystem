-- Add Values --
INSERT ALL
    INTO doctors VALUES (1, 'Abdelrahman Khalifa')
    INTO doctors VALUES (2, 'Ahmed Zahra')
SELECT 1 FROM dual;

INSERT ALL
    INTO courses VALUES (1, 'Pathology', 1)
    INTO courses VALUES (2, 'Histology', 2)
SELECT 1 FROM dual;

INSERT ALL
    INTO students VALUES (1, 'Omar')
    INTO students VALUES (2, 'Mohamed')
    INTO students VALUES (3, 'Yousef')
    INTO students VALUES (4, 'Ziad')
    INTO students VALUES (5, 'Maged')
    INTO students VALUES (6, 'Khaled')
SELECT 1 FROM dual;

INSERT ALL
    INTO student_enrollment VALUES (1, 1, 1)
    INTO student_enrollment VALUES (2, 1, 2)
    INTO student_enrollment VALUES (3, 2, 2)
    INTO student_enrollment VALUES (4, 3, 2)
    INTO student_enrollment VALUES (5, 4, 1)
    INTO student_enrollment VALUES (6, 6, 1)
    INTO student_enrollment VALUES (7, 6, 2)
SELECT 1 FROM dual;

INSERT ALL
    INTO payments VALUES (1, 1, 1)
    INTO payments VALUES (2, 1, 2)
    INTO payments VALUES (3, 2, 2)
    INTO payments VALUES (4, 3, 2)
    INTO payments VALUES (5, 4, 1)
    INTO payments VALUES (6, 6, 1)
    INTO payments VALUES (7, 6, 2)
    INTO payments VALUES (8, 1, 2)
SELECT 1 FROM dual;

-- Query The Database --
SELECT * FROM students;
SELECT * FROM courses;
SELECT * FROM doctors;
SELECT * FROM student_enrollment;
SELECT * FROM payments;

SELECT s.name AS Student, c.name AS Course, d.name AS Doctor
FROM students s JOIN student_enrollment ON s.id = student_enrollment.student_id
JOIN courses c ON c.id = student_enrollment.course_id
JOIN doctors d ON c.doctor_id = d.id;