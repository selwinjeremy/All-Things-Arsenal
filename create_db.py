import mysql.connector

mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd = x
)

my_cursor = mydatabase.cursor()

#my_cursor.execute("CREATE DATABASE arsenalStats")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)


