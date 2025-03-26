import pymysql

try:
    conn = pymysql.connect(
        host="visidel.org",
        user="james",
        password="ibm2024#",
        port=3310,
        database="dogui"
    )
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print("Error:", e)
