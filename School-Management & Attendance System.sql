


-- ==========================================
-- SCHOOL MANAGEMENT SYSTEM DATABASE
-- PyMySQL Project
-- ==========================================

DROP DATABASE IF EXISTS school_database;

CREATE DATABASE school_database;

USE school_database;



-- CLASS TABLE

CREATE TABLE classes(

    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(20) UNIQUE NOT NULL

);

-- ==========================================
-- STUDENTS TABLE
-- ==========================================

CREATE TABLE students(

    student_id INT AUTO_INCREMENT PRIMARY KEY,

    student_name VARCHAR(50) NOT NULL,

    roll_no INT NOT NULL,

    city VARCHAR(50),

    class_id INT NOT NULL,

    FOREIGN KEY(class_id)
    REFERENCES classes(class_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    UNIQUE(class_id,roll_no)

);

-- ==========================================
-- ATTENDANCE TABLE
-- ==========================================

CREATE TABLE attendance(

    attendance_id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,
   

    attendance_date DATE NOT NULL,

    status ENUM('P','A') NOT NULL,

    FOREIGN KEY(student_id)
    REFERENCES students(student_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    UNIQUE(student_id,attendance_date)

);



ALTER TABLE attendance
ADD COLUMN STUDENT_NAME VARCHAR(30);

-- ==========================================
-- INSERT DEFAULT CLASSES
-- ==========================================

INSERT INTO classes(class_name)
VALUES

('Python'),
('MY_SQL'),
('EXCEL'),
('VBA'),
('POER_BI'),
('TABLEAU'),
('NUMPY')
;



-- ==========================================
-- SAMPLE STUDENTS
-- ==========================================

INSERT INTO students(student_name,roll_no,city,class_id)
VALUES

('Rahul',1,'Delhi',10),
('Rohit',2,'Delhi',10),
('Ankit',3,'Jaipur',10),
('Karan',1,'Mumbai',9),
('Neha',2,'Noida',9),
('Pooja',1,'Agra',8);

-- ==========================================
-- SAMPLE ATTENDANCE
-- ==========================================

INSERT INTO attendance(student_id,attendance_date,status)
VALUES

(1,CURDATE(),'P'),
(2,CURDATE(),'A'),
(3,CURDATE(),'P'),
(4,CURDATE(),'P'),
(5,CURDATE(),'A'),
(6,CURDATE(),'P');

-- ==========================================
-- VIEW : STUDENT DETAILS
-- ==========================================

CREATE VIEW student_details AS

SELECT

s.student_id,
s.student_name,
s.roll_no,
s.city,
c.class_name

FROM students s

JOIN classes c

ON s.class_id=c.class_id;

-- ==========================================
-- VIEW : ATTENDANCE REPORT
-- ==========================================

CREATE VIEW attendance_report AS

SELECT

s.student_name,
s.roll_no,
c.class_name,

COUNT(a.attendance_id) AS Total_Days,

SUM(CASE
WHEN a.status='P'
THEN 1
ELSE 0
END) AS Present_Days,

SUM(CASE
WHEN a.status='A'
THEN 1
ELSE 0
END) AS Absent_Days,

ROUND(

SUM(CASE
WHEN a.status='P'
THEN 1
ELSE 0
END)

*100/

COUNT(a.attendance_id)

,2)

AS Attendance_Percentage

FROM students s

JOIN attendance a

ON s.student_id=a.student_id

JOIN classes c

ON s.class_id=c.class_id

GROUP BY s.student_id;

-- ==========================================
-- USEFUL QUERIES
-- ==========================================

-- View Students

SELECT *
FROM student_details;

-- Class Wise Students

SELECT *

FROM student_details

WHERE class_name='10th';

-- Search Student

SELECT *

FROM student_details

WHERE student_name='Rahul';

-- Total Students

SELECT COUNT(*)

FROM students

WHERE class_id=10;

-- Attendance History

SELECT

attendance_date,
status

FROM attendance

WHERE student_id=1

ORDER BY attendance_date;

-- Attendance %

SELECT *

FROM attendance_report

WHERE roll_no=1;

-- ==========================================
-- END
-- ==========================================


USE SCHOOL_DATABASE;

SELECT * FROM STUDENTS;
SELECT * FROM CLASSES ORDER BY CLASS_ID ASC;
SELECT * FROM ATTENDANCE;



