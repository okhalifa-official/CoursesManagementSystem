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
    ), 0)) || ' EGP' AS Remaining,
    c.enrollment_date AS 'Date'
FROM student_course c
JOIN students s ON c.student_id = s.id
WHERE (c.course_price - IFNULL((
            SELECT SUM(p.amount_paid)
            FROM payments p
            WHERE p.student_course_id = c.id
        ), 0)) > 0;


SELECT 
    sc.course_name AS 'Course Name', 
    p.amount_paid || ' EGP' AS 'Amount Paid', 
    p.payment_type AS 'Payment Type', 
    sc.course_price || ' EGP' AS 'Total',
    p.payment_date AS 'Transaction Date'
FROM students s
JOIN student_course sc ON s.id = sc.student_id
JOIN payments p ON p.student_course_id = sc.id
WHERE s.id = 1;

SELECT c.name AS 'Course Name'
FROM courses c
WHERE c.id NOT IN (
    SELECT sc.course_id
    FROM student_course sc
    WHERE sc.student_id = 1
);

-- total enrolled students, total paid, total remaining, total expected
SELECT COUNT(*) AS 'No Enrolled Students', SUM(p.amount_paid) || ' EGP' AS 'Total Amount Paid', 
        COUNT(*)*c.course_price-SUM(p.amount_paid) || ' EGP' AS 'Total Remaining', 
        COUNT(*)*c.course_price || ' EGP' AS 'Total Expected'
FROM 