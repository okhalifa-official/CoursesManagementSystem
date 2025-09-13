-- Query The Database --
SELECT * FROM students;
SELECT * FROM courses;
SELECT * FROM doctors;
SELECT * FROM student_enrollment;
SELECT * FROM payments;

SELECT s.id AS id, s.name AS Student, c.name AS Course, d.name AS Doctor, payments.id AS 'Payment ID'
FROM payments, students s JOIN student_enrollment ss ON s.id = ss.student_id
JOIN courses c ON ss.course_id = c.id
JOIN doctors d ON c.doctor_id = d.id
WHERE payments.course_id = c.id AND payments.student_id = s.id
ORDER BY s.id;