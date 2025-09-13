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

UPDATE courses
SET name = 'Histology of Kidney'
WHERE name = 'Histology';

UPDATE doctors
SET name = 'Dr. Abdelrahman Khalifa'
WHERE id = 1;