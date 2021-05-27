import mysql.connector as mariadb

# Module Imports

import sys

# Connect to MariaDB Platform
try:
      conn = mariadb.connect(
        user="remote_connect",
        password="remote_connect",
        host="34.72.114.168",
        port=3306,
        database="wordpress"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
cursor = conn.cursor()
cursor.execute("SELECT * FROM Attendance")
print(cursor)
for Name in cursor:
   print(Name)

date="2020-11-19"
staff_id=12144
Name="HARPAL SINGH"
Attend="P"

#cursor.execute("INSERT INTO Attendance (date,staff_id,Name,Attend) VALUES (%s,%s,%s,%s)", (date, staff_id, Name, Attend))
#conn.commit()

conn.close()