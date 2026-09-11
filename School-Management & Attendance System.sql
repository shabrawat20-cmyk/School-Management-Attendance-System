-- ==========================================
-- SCHOOL MANAGEMENT & ATTENDANCE SYSTEM
-- MySQL Database Setup
-- ==========================================

CREATE DATABASE IF NOT EXISTS school_database;
USE school_database;



CREATE TABLE IF NOT EXISTS classes(
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS students(
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(50) NOT NULL,
    roll_no INT NOT NULL,
    city VARCHAR(50),
    class_id INT NOT NULL,
    FOREIGN KEY(class_id) REFERENCES classes(class_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE(class_id, roll_no)
);

CREATE TABLE IF NOT EXISTS attendance(
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status ENUM('P','A') NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE(student_id, attendance_date)
);

-- Default classes
INSERT IGNORE INTO classes(class_name)
VALUES ('9th'), ('10th'), ('11th'), ('12th');

-- Sample students
INSERT IGNORE INTO students(student_name, roll_no, city, class_id)
SELECT 'Rahul', 1, 'Delhi', class_id FROM classes WHERE class_name='10th';
INSERT IGNORE INTO students(student_name, roll_no, city, class_id)
SELECT 'Rohit', 2, 'Delhi', class_id FROM classes WHERE class_name='10th';
INSERT IGNORE INTO students(student_name, roll_no, city, class_id)
SELECT 'Ankit', 3, 'Jaipur', class_id FROM classes WHERE class_name='10th';
INSERT IGNORE INTO students(student_name, roll_no, city, class_id)
SELECT 'Karan', 1, 'Mumbai', class_id FROM classes WHERE class_name='9th';
INSERT IGNORE INTO students(student_name, roll_no, city, class_id)
SELECT 'Neha', 2, 'Noida', class_id FROM classes WHERE class_name='9th';
INSERT IGNORE INTO students(student_name, roll_no, city, class_id)
SELECT 'Pooja', 1, 'Agra', class_id FROM classes WHERE class_name='11th';

-- Sample attendance
INSERT INTO attendance(student_id, attendance_date, status)
SELECT student_id, CURDATE(), 'P' FROM students WHERE student_name='Rahul' AND roll_no=1
ON DUPLICATE KEY UPDATE status=VALUES(status);
INSERT INTO attendance(student_id, attendance_date, status)
SELECT student_id, CURDATE(), 'A' FROM students WHERE student_name='Rohit' AND roll_no=2
ON DUPLICATE KEY UPDATE status=VALUES(status);
INSERT INTO attendance(student_id, attendance_date, status)
SELECT student_id, CURDATE(), 'P' FROM students WHERE student_name='Ankit' AND roll_no=3
ON DUPLICATE KEY UPDATE status=VALUES(status);
INSERT INTO attendance(student_id, attendance_date, status)
SELECT student_id, CURDATE(), 'P' FROM students WHERE student_name='Karan' AND roll_no=1
ON DUPLICATE KEY UPDATE status=VALUES(status);
INSERT INTO attendance(student_id, attendance_date, status)
SELECT student_id, CURDATE(), 'A' FROM students WHERE student_name='Neha' AND roll_no=2
ON DUPLICATE KEY UPDATE status=VALUES(status);
INSERT INTO attendance(student_id, attendance_date, status)
SELECT student_id, CURDATE(), 'P' FROM students WHERE student_name='Pooja' AND roll_no=1
ON DUPLICATE KEY UPDATE status=VALUES(status);

-- Student details view
CREATE OR REPLACE VIEW student_details AS
SELECT s.student_id, s.student_name, s.roll_no, s.city, c.class_name
FROM students s
JOIN classes c ON s.class_id=c.class_id;

-- Attendance report view
CREATE OR REPLACE VIEW attendance_report AS
SELECT s.student_name, s.roll_no, c.class_name,
       COUNT(a.attendance_id) AS Total_Days,
       SUM(CASE WHEN a.status='P' THEN 1 ELSE 0 END) AS Present_Days,
       SUM(CASE WHEN a.status='A' THEN 1 ELSE 0 END) AS Absent_Days,
       ROUND(SUM(CASE WHEN a.status='P' THEN 1 ELSE 0 END)*100.0 /
             NULLIF(COUNT(a.attendance_id),0), 2) AS Attendance_Percentage
FROM students s
JOIN attendance a ON s.student_id=a.student_id
JOIN classes c ON s.class_id=c.class_id
GROUP BY s.student_id, s.student_name, s.roll_no, c.class_name;

-- Useful queries
SELECT * FROM student_details;
SELECT * FROM student_details WHERE class_name='10th';
SELECT * FROM student_details WHERE student_name='Rahul';
SELECT COUNT(*) AS Total_Students FROM students;
SELECT s.student_name, a.attendance_date, a.status
FROM attendance a JOIN students s ON a.student_id=s.student_id
ORDER BY a.attendance_date;
SELECT * FROM attendance_report;

-- ==========================================
-- END
-- ==========================================
