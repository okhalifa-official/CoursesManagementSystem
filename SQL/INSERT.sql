INSERT INTO students (id, first_name, last_name, gender, country_code, phone_number, university, barcode, email, address)
VALUES
(3, 'Youssef', 'Mahmoud', 'Male', '+971', '0501122334', 'AUC', 'STU003', 'youssef.mahmoud@example.com', 'Dubai, UAE'),
(4, 'Laila', 'Omar', 'Female', '+966', '0556677889', 'King Saud University', 'STU004', 'laila.omar@example.com', 'Riyadh, KSA'),
(5, 'Karim', 'Ali', 'Male', '+20', '01055556666', 'Alex University', 'STU005', 'karim.ali@example.com', 'Alexandria, Egypt');

INSERT INTO doctors (id, first_name, last_name, gender, email, country_code, phone_number)
VALUES
(3, 'Hany', 'Mostafa', 'Male', 'hany.mostafa@univ.edu', '+971', '0509988776'),
(4, 'Nour', 'Samir', 'Female', 'nour.samir@univ.edu', '+966', '0554433221'),
(5, 'Tarek', 'Younis', 'Male', 'tarek.younis@univ.edu', '+20', '01077778888');

INSERT INTO courses (id, name, doctor_id, price, start_date, end_date)
VALUES
(3, 'Machine Learning', 3, 7000, '2025-11-01', '2026-02-01'),
(4, 'Operating Systems', 4, 4500, '2025-10-15', '2026-01-05'),
(5, 'Computer Networks', 5, 4000, '2025-09-30', '2025-12-20');

INSERT INTO student_course (id, student_id, doctor_id, course_name, course_price, course_start_date, course_end_date, enrollment_date, course_id)
VALUES
(3, 3, 3, 'Machine Learning', 7000, '2025-11-01', '2026-02-01', '2025-09-28', 3),
(4, 4, 4, 'Operating Systems', 4500, '2025-10-15', '2026-01-05', '2025-09-29', 4),
(5, 5, 5, 'Computer Networks', 4000, '2025-09-30', '2025-12-20', '2025-09-21', 5),
(6, 2, 5, 'Computer Networks', 4000, '2025-09-30', '2025-12-20', '2025-09-25', 5); -- Sara enrolled in an extra course

INSERT INTO payments (id, student_id, student_course_id, payment_date, amount_paid)
VALUES
(4, 3, 3, '2025-09-30', 3500),   -- Youssef paid half for ML
(5, 3, 3, '2025-10-20', 3500),   -- Youssef completed ML
(6, 4, 4, '2025-09-29', 4500),   -- Laila paid full for OS
(7, 5, 5, '2025-09-22', 2000),   -- Karim paid part of Networks
(8, 5, 5, '2025-10-05', 2000),   -- Karim completed Networks
(9, 2, 6, '2025-09-25', 4000);   -- Sara paid full for her second course (Networks)
