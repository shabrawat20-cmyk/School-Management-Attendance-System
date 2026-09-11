import os
import pymysql
from getpass import getpass
from datetime import date
import pandas as pd

DB_HOST = os.getenv("DB_HOST","localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_NAME = "school_database"

db_password = os.getenv("DB_PASSWORD")

if not db_password:
    db_password = getpass("Enter MySQL Password : ")

try:
    con = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=db_password
    )

    cur = con.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS school_database")
    cur.execute("USE school_database")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS classes(
        class_id INT AUTO_INCREMENT PRIMARY KEY,
        class_name VARCHAR(20) UNIQUE NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        student_id INT AUTO_INCREMENT PRIMARY KEY,
        student_name VARCHAR(50) NOT NULL,
        roll_no INT NOT NULL,
        city VARCHAR(50),
        class_id INT NOT NULL,
        FOREIGN KEY(class_id) REFERENCES classes(class_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
        UNIQUE(class_id,roll_no)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        attendance_id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT NOT NULL,
        attendance_date DATE NOT NULL,
        status ENUM('P','A') NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
        UNIQUE(student_id,attendance_date)
    )
    """)

    cur.execute("SELECT COUNT(*) FROM classes")
    class_total = cur.fetchone()[0]

    if class_total == 0:
        cur.executemany(
            "INSERT INTO classes(class_name) VALUES(%s)",
            [("9th",),("10th",),("11th",),("12th",)]
        )
        con.commit()

    print("\nConnected To School Database")

except Exception as e:
    print("\nDatabase Connection Error :", e)
    raise SystemExit


# login
def school_login():

    username = input("Enter Username : ")
    password = getpass("Enter Password : ")

    admin_user = "Ducat"
    admin_password = "Ducat2026"

    if username == admin_user and password == admin_password:

        print("\nLogin Successful\n")
        return True

    else:

        print("\nInvalid Username or Password\n")
        return False


# helper
def get_number(message):

    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please Enter Valid Number")


def show_classes():

    cur.execute("SELECT class_id,class_name FROM classes ORDER BY class_id")
    data = cur.fetchall()

    print("\nAvailable Classes\n")

    for i in data:
        print(i[0], "-", i[1])


# create menu
def menu():

    print("\n")
    print("=" * 48)
    print("       SCHOOL MANAGEMENT SYSTEM")
    print("=" * 48)

    print("1. Add Student")
    print("2. View Students")
    print("3. Take Attendance")
    print("4. Search Student")
    print("5. Delete Student")
    print("6. Update Student")
    print("7. Total Students")
    print("8. Search By Name")
    print("9. Attendance Report")
    print("10. Student Attendance History")
    print("11. Low Attendance Students")
    print("12. Export Students to CSV")
    print("13. School Dashboard")
    print("14. Exit")

    print("=" * 48)


# add student
def add_student():

    print("\n========== ADD STUDENT ==========\n")

    name = input("Enter Student Name : ").strip()

    if name == "":
        print("Name Cannot Be Empty")
        return

    roll = get_number("Enter Roll Number : ")

    city = input("Enter City : ").strip()

    show_classes()

    class_id = get_number("\nEnter Class ID : ")

    cur.execute("SELECT class_id FROM classes WHERE class_id=%s", (class_id,))

    if cur.fetchone() is None:
        print("Invalid Class ID")
        return

    query = """
    INSERT INTO students(student_name,roll_no,city,class_id)
    VALUES(%s,%s,%s,%s)
    """

    values = (name, roll, city, class_id)

    try:

        cur.execute(query, values)

        con.commit()

        print("\nStudent Added Successfully.\n")

    except pymysql.MySQLError as e:

        con.rollback()
        print("\nStudent Not Added :", e)


# view student
def view_students():

    print("\n========== VIEW STUDENTS ==========\n")

    class_name = input("Enter Class Name (Example 10th) : ").strip()

    query = """

    SELECT
    s.student_id,
    s.student_name,
    s.roll_no,
    s.city

    FROM students s

    JOIN classes c

    ON s.class_id=c.class_id

    WHERE c.class_name=%s

    ORDER BY s.roll_no
    """

    cur.execute(query, (class_name,))

    students = cur.fetchall()

    if len(students) == 0:

        print("No Students Found")

    else:

        print("\nID\tRoll\tName\t\tCity")
        print("-" * 50)

        for i in students:

            print(i[0], "\t", i[2], "\t", i[1], "\t", i[3])


# search student
def search_student():

    print("\n========== SEARCH STUDENT ==========\n")

    class_name = input("Enter Class : ").strip()

    roll = get_number("Enter Roll Number : ")

    query = """

    SELECT
    s.student_id,
    s.student_name,
    s.roll_no,
    s.city,
    c.class_name

    FROM students s

    JOIN classes c

    ON s.class_id=c.class_id

    WHERE c.class_name=%s

    AND s.roll_no=%s
    """

    cur.execute(query, (class_name, roll))

    student = cur.fetchone()

    if student:

        print("\nStudent Found\n")
        print("ID :", student[0])
        print("Name :", student[1])
        print("Roll :", student[2])
        print("City :", student[3])
        print("Class :", student[4])

    else:

        print("\nStudent Not Found")


# delete student
def delete_student():

    print("\n========== DELETE STUDENT ==========\n")

    class_name = input("Enter Class : ").strip()

    roll = get_number("Enter Roll Number : ")

    query = """

    DELETE s

    FROM students s

    JOIN classes c

    ON s.class_id=c.class_id

    WHERE c.class_name=%s

    AND s.roll_no=%s
    """

    try:

        cur.execute(query, (class_name, roll))

        con.commit()

        if cur.rowcount > 0:

            print("\nStudent Deleted Successfully")

        else:

            print("\nStudent Not Found")

    except pymysql.MySQLError as e:

        con.rollback()
        print("Delete Error :", e)


# update Detail
def update_student():

    print("\n========== UPDATE STUDENT ==========\n")

    class_name = input("Enter Class : ").strip()

    roll = get_number("Enter Roll Number : ")

    query = """

    SELECT s.student_id

    FROM students s

    JOIN classes c

    ON s.class_id=c.class_id

    WHERE c.class_name=%s

    AND s.roll_no=%s
    """

    cur.execute(query, (class_name, roll))

    data = cur.fetchone()

    if data is None:

        print("Student Not Found")
        return

    print("\n1. Update Name")
    print("2. Update Roll Number")
    print("3. Update City")

    ch = input("Choice : ")

    try:

        if ch == "1":

            new_name = input("Enter New Name : ").strip()

            cur.execute(
                "UPDATE students SET student_name=%s WHERE student_id=%s",
                (new_name, data[0])
            )

        elif ch == "2":

            new_roll = get_number("Enter New Roll : ")

            cur.execute(
                "UPDATE students SET roll_no=%s WHERE student_id=%s",
                (new_roll, data[0])
            )

        elif ch == "3":

            city = input("Enter New City : ").strip()

            cur.execute(
                "UPDATE students SET city=%s WHERE student_id=%s",
                (city, data[0])
            )

        else:

            print("Invalid Choice")
            return

        con.commit()

        print("\nUpdated Successfully")

    except pymysql.MySQLError as e:

        con.rollback()
        print("Update Error :", e)


# total student
def total_students():

    print("\n========== TOTAL STUDENTS ==========\n")

    class_name = input("Enter Class : ").strip()

    query = """

    SELECT COUNT(*)

    FROM students s

    JOIN classes c

    ON s.class_id=c.class_id

    WHERE c.class_name=%s
    """

    cur.execute(query, (class_name,))

    total = cur.fetchone()

    print("\nTotal Students :", total[0])


# search
def search_by_name():

    print("\n========== SEARCH BY NAME ==========\n")

    name = input("Enter Student Name : ").strip()

    query = """

    SELECT
    s.student_name,
    s.roll_no,
    s.city,
    c.class_name

    FROM students s

    JOIN classes c

    ON s.class_id=c.class_id

    WHERE s.student_name LIKE %s

    ORDER BY c.class_name,s.roll_no
    """

    cur.execute(query, ("%" + name + "%",))

    data = cur.fetchall()

    if len(data) == 0:

        print("No Record Found")

    else:

        print("\nName\tRoll\tCity\tClass")
        print("-" * 50)

        for i in data:

            print(i[0], "\t", i[1], "\t", i[2], "\t", i[3])


# attendance
def take_attendance():

    print("\n========== TAKE ATTENDANCE ==========\n")

    class_name = input("Enter Class : ").strip()

    query = """

    SELECT
    s.student_id,
    s.roll_no,
    s.student_name

    FROM students s

    JOIN classes c

    ON s.class_id=c.class_id

    WHERE c.class_name=%s

    ORDER BY s.roll_no
    """

    cur.execute(query, (class_name,))

    students = cur.fetchall()

    if len(students) == 0:

        print("No Students Found")
        return

    today = date.today()

    print("\nAttendance Date :", today)

    for student in students:

        print("\n-----------------------")

        print("Roll :", student[1])
        print("Name :", student[2])

        status = input("Attendance (P/A) : ").upper()

        while status not in ["P", "A"]:

            status = input("Enter Only P or A : ").upper()

        check = """
        SELECT attendance_id
        FROM attendance
        WHERE student_id=%s AND attendance_date=%s
        """

        cur.execute(check, (student[0], today))

        old_data = cur.fetchone()

        if old_data:

            update = """
            UPDATE attendance
            SET status=%s
            WHERE student_id=%s
            AND attendance_date=%s
            """

            cur.execute(update, (status, student[0], today))

        else:

            insert = """
            INSERT INTO attendance
            (student_id,attendance_date,status)

            VALUES(%s,%s,%s)
            """

            cur.execute(insert, (student[0], today, status))

    con.commit()

    print("\nAttendance Saved Successfully.")


# attendance report
def attendance_report():

    print("\n========== ATTENDANCE REPORT ==========\n")

    class_name = input("Enter Class : ").strip()

    roll = get_number("Enter Roll Number : ")

    query = """

    SELECT
    s.student_name,

    COUNT(a.attendance_id),

    SUM(CASE WHEN a.status='P' THEN 1 ELSE 0 END),

    SUM(CASE WHEN a.status='A' THEN 1 ELSE 0 END),

    ROUND(

    SUM(CASE WHEN a.status='P' THEN 1 ELSE 0 END)

    *100/

    COUNT(a.attendance_id)

    ,2)

    FROM students s

    JOIN attendance a

    ON s.student_id=a.student_id

    JOIN classes c

    ON s.class_id=c.class_id

    WHERE

    c.class_name=%s

    AND

    s.roll_no=%s

    GROUP BY s.student_id
    """

    cur.execute(query, (class_name, roll))

    data = cur.fetchone()

    if data:

        print("\nName :", data[0])
        print("Total Days :", data[1])
        print("Present :", data[2])
        print("Absent :", data[3])
        print("Attendance :", data[4], "%")

        if data[4] < 75:
            print("Status : LOW ATTENDANCE")

    else:

        print("No Record Found")


# attendance history by date
def attendance_history():

    print("\n========== ATTENDANCE HISTORY ==========\n")

    class_name = input("Enter Class : ").strip()

    roll = get_number("Enter Roll Number : ")

    query = """

    SELECT
    a.attendance_date,

    a.status

    FROM attendance a

    JOIN students s

    ON a.student_id=s.student_id

    JOIN classes c

    ON s.class_id=c.class_id

    WHERE

    c.class_name=%s

    AND

    s.roll_no=%s

    ORDER BY attendance_date
    """

    cur.execute(query, (class_name, roll))

    history = cur.fetchall()

    if len(history) == 0:

        print("No Attendance Found")

    else:

        print("\nDate\t\tStatus")
        print("-" * 30)

        for i in history:

            print(i[0], "\t", i[1])


# low attendance
def low_attendance():

    print("\n========== LOW ATTENDANCE STUDENTS ==========\n")

    query = """

    SELECT
    s.student_name,
    s.roll_no,
    c.class_name,

    ROUND(
        SUM(CASE WHEN a.status='P' THEN 1 ELSE 0 END)
        * 100 / COUNT(a.attendance_id)
    ,2) AS attendance_percentage

    FROM students s

    JOIN attendance a
    ON s.student_id=a.student_id

    JOIN classes c
    ON s.class_id=c.class_id

    GROUP BY s.student_id,s.student_name,s.roll_no,c.class_name

    HAVING attendance_percentage < 75

    ORDER BY attendance_percentage
    """

    cur.execute(query)

    data = cur.fetchall()

    if len(data) == 0:

        print("No Low Attendance Students Found")

    else:

        print("Name\tRoll\tClass\tAttendance")
        print("-" * 55)

        for i in data:

            print(i[0], "\t", i[1], "\t", i[2], "\t", i[3], "%")


# export csv
def export_students():

    print("\n========== EXPORT CSV ==========\n")

    print("1. Class Wise")
    print("2. Complete Database")
    print("3. Attendance Report")

    ch = input("Choice : ")

    os.makedirs("exports", exist_ok=True)

    if ch == "1":

        class_name = input("Enter Class : ").strip()

        query = """

        SELECT
        s.student_name,
        s.roll_no,
        s.city,
        c.class_name

        FROM students s

        JOIN classes c

        ON s.class_id=c.class_id

        WHERE c.class_name=%s
        """

        df = pd.read_sql(query, con, params=[class_name])

        file_name = os.path.join("exports", class_name + "_Students.csv")

        df.to_csv(file_name, index=False)

        print(file_name, "Created Successfully")

    elif ch == "2":

        query = "SELECT * FROM student_details"

        df = pd.read_sql(query, con)

        file_name = os.path.join("exports", "All_Students.csv")

        df.to_csv(file_name, index=False)

        print(file_name, "Created Successfully")

    elif ch == "3":

        df = pd.read_sql("SELECT * FROM attendance_report", con)

        file_name = os.path.join("exports", "Attendance_Report.csv")

        df.to_csv(file_name, index=False)

        print(file_name, "Created Successfully")

    else:

        print("Invalid Choice")


# school dashboard
def school_dashboard():

    print("\n========== SCHOOL DASHBOARD ==========\n")

    cur.execute("SELECT COUNT(*) FROM students")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM classes")
    total_classes = cur.fetchone()[0]

    today = date.today()

    cur.execute(
        "SELECT COUNT(*) FROM attendance WHERE attendance_date=%s AND status='P'",
        (today,)
    )
    present = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM attendance WHERE attendance_date=%s AND status='A'",
        (today,)
    )
    absent = cur.fetchone()[0]

    attendance_rate = 0

    if present + absent > 0:
        attendance_rate = round(present * 100 / (present + absent), 2)

    print("Total Students    :", total)
    print("Total Classes     :", total_classes)
    print("Present Today     :", present)
    print("Absent Today      :", absent)
    print("Attendance Rate   :", attendance_rate, "%")

    print("\nCLASS WISE STUDENTS")
    print("-" * 35)

    query = """
    SELECT
    c.class_name,
    COUNT(s.student_id)

    FROM classes c

    LEFT JOIN students s
    ON c.class_id=s.class_id

    GROUP BY c.class_id,c.class_name
    ORDER BY c.class_id
    """

    cur.execute(query)

    data = cur.fetchall()

    for i in data:

        print(i[0], ":", i[1])


# login system
def start_project():

    if school_login():

        while True:

            menu()

            choice = input("Enter Choice : ")

            if choice == "1":
                add_student()

            elif choice == "2":
                view_students()

            elif choice == "3":
                take_attendance()

            elif choice == "4":
                search_student()

            elif choice == "5":
                delete_student()

            elif choice == "6":
                update_student()

            elif choice == "7":
                total_students()

            elif choice == "8":
                search_by_name()

            elif choice == "9":
                attendance_report()

            elif choice == "10":
                attendance_history()

            elif choice == "11":
                low_attendance()

            elif choice == "12":
                export_students()

            elif choice == "13":
                school_dashboard()

            elif choice == "14":

                print("\nThank You\n")

                cur.close()
                con.close()

                break

            else:

                print("Invalid Choice")


if __name__ == "__main__":

    start_project()
