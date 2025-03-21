import mysql.connector

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host= "visidel.org",             # Your database host (e.g., localhost)
    user= "dylan",           # Your database username
    password= "dogui_new@2025",         # Your data password
    database= "dogui",          # Your database name
    port=  "3310"                  # Your database port
)

# Create a cursor object to interact with the database
cursor = db_connection.cursor()

# Execute  a SELECT query
cursor.execute("SELECT id, name, age FROM students")

# Fetch all rows from the result of the query
students = cursor.fetchall()

# Loop through and print the rows
for student in students:
    print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}")

# Close the cursor and connection
cursor.close()
db_connection.close()