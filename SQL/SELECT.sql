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

SELECT 
    c.course_name AS 'Course Name', 
    (c.course_price - IFNULL((
        SELECT SUM(p.amount_paid)
        FROM payments p
        WHERE p.student_course_id = c.id
    ), 0)) AS Remaining,
    c.enrollment_date AS 'Date'
FROM student_course c
JOIN students s ON c.student_id = s.id;


SELECT 
    sc.course_name AS 'Course Name', 
    p.amount_paid AS 'Amount Paid', 
    p.payment_type AS 'Payment Type', 
    sc.course_price AS 'Total',
    p.payment_date AS 'Transaction Date'
FROM students s
JOIN student_course sc ON s.id = sc.student_id
JOIN payments p ON p.student_course_id = sc.id
WHERE s.id = 1;