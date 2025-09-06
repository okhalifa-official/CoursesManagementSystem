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