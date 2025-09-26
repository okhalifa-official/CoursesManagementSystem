-- Students
INSERT INTO students (id, first_name, last_name, gender, country_code, phone_number, address, email, university, barcode)
VALUES
(3, 'Youssef', 'Mahmoud', 'Male', '+971', '0501122334', 'Dubai, UAE', 'youssef.mahmoud@example.com', 'AUC', 'STU003'),
(4, 'Laila', 'Omar', 'Female', '+966', '0556677889', 'Riyadh, KSA', 'laila.omar@example.com', 'King Saud University', 'STU004'),
(5, 'Karim', 'Ali', 'Male', '+20', '01055556666', 'Alexandria, Egypt', 'karim.ali@example.com', 'Alex University', 'STU005'),
(6, 'Mona', 'Hassan', 'Female', '+20', '01012345678', 'Cairo, Egypt', 'mona.hassan@example.com', 'Cairo University', 'STU006');

-- Doctors
INSERT INTO doctors (id, first_name, last_name, gender, email, country_code, phone_number)
VALUES
(3, 'Hany', 'Mostafa', 'Male', 'hany.mostafa@univ.edu', '+971', '0509988776'),
(4, 'Nour', 'Samir', 'Female', 'nour.samir@univ.edu', '+966', '0554433221'),
(5, 'Tarek', 'Younis', 'Male', 'tarek.younis@univ.edu', '+20', '01077778888');

-- Courses
INSERT INTO courses (id, name, doctor_id, price, start_date, end_date)
VALUES
(3, 'Machine Learning', 3, 7000, '2025-11-01', '2026-02-01'),
(4, 'Operating Systems', 4, 4500, '2025-10-15', '2026-01-05'),
(5, 'Computer Networks', 5, 4000, '2025-09-30', '2025-12-20');

-- Student Course
INSERT INTO student_course (id, student_id, doctor_id, course_name, course_price, course_start_date, course_end_date, enrollment_date, course_id)
VALUES
(3, 3, 3, 'Machine Learning', 7000, '2025-11-01', '2026-02-01', '2025-09-28', 3),
(4, 4, 4, 'Operating Systems', 4500, '2025-10-15', '2026-01-05', '2025-09-29', 4),
(5, 5, 5, 'Computer Networks', 4000, '2025-09-30', '2025-12-20', '2025-09-21', 5),
(6, 2, 5, 'Computer Networks', 4000, '2025-09-30', '2025-12-20', '2025-09-25', 5),
(7, 6, 3, 'Machine Learning', 7000, '2025-11-01', '2026-02-01', '2025-10-01', 3),
(8, 6, 5, 'Computer Networks', 4000, '2025-09-30', '2025-12-20', '2025-10-02', 5);

-- Payments
INSERT INTO payments (id, student_id, student_course_id, payment_date, payment_type, amount_paid)
VALUES
(4, 3, 3, '2025-09-30', 'Cash', 3500),   -- Youssef paid half for ML
(5, 3, 3, '2025-10-20', 'Cash', 3500),   -- Youssef completed ML
(6, 4, 4, '2025-09-29', 'Visa', 4500),   -- Laila paid full for OS
(7, 5, 5, '2025-09-22', 'Cash', 2000),   -- Karim paid part of Networks
(8, 5, 5, '2025-10-05', 'Cash', 2000),   -- Karim completed Networks
(9, 2, 6, '2025-09-25', 'Instapay', 4000),   -- Sara paid full for her second course (Networks)
(10, 6, 7, '2025-10-05', 'Vodafone Cash', 2000),  -- Mona partial ML
(11, 6, 8, '2025-10-06', 'Cash', 1000);           -- Mona partial Networks