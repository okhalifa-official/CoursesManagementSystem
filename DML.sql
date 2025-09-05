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

SELECT s.name AS Student, c.name AS Course, d.name AS Doctor, se.id
FROM students s JOIN payments se ON s.id = se.student_id
JOIN courses c ON c.id = se.course_id
JOIN doctors d ON c.doctor_id = d.id
ORDER BY s.id;

-- Update Values --
UPDATE students
SET name = 'Mazen'
WHERE name = 'Maged';

BEGIN
    UPDATE student_enrollment
    SET course_id = 1
    WHERE student_id = 3 AND course_id = 2;

    UPDATE payments
    SET course_id = 1
    WHERE student_id = 3 AND course_id = 2;
END;
/

UPDATE courses
SET name = 'Histology of Kidney'
WHERE name = 'Histology';

UPDATE doctors
SET name = 'Dr. Abdelrahman Khalifa'
WHERE id = 1;

-- Remove Records --

DELETE FROM students
WHERE name LIKE '%ed';

DELETE FROM courses
WHERE id = 3;

DELETE FROM doctors
WHERE id = 4;

BEGIN
    DELETE FROM student_enrollment
    WHERE student_id = 1 AND course_id = 2;

    DELETE FROM payments
    WHERE student_id = 1 AND course_id = 2;
END;
/
