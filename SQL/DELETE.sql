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