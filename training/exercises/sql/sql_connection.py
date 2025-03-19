import mysql.connector

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="[HOST]",        # Your database host (e.g., localhost)
    user="[username]",             # Your database username
    password="[pass]",  # Your database password
    database="[db]",     # Your database name
    port="[port]"
)

# Create a cursor object to interact with the database
cursor = db_connection.cursor()

# Execute a SELECT query
cursor.execute("SELECT id, {name}, age FROM students")

# Fetch all rows from the result of the query
students = cursor.fetchall()

# Loop through and print the rows
for student in students:
    print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}")

# Close the cursor and connection
cursor.close()
db_connection.close()
