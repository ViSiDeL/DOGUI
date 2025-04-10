import pymysql

try:
    conn = pymysql.connect(
        host="visidel.org",
        user="[SECRET]",
        password="[SECRET]",
        port=[SECRET],
        database="[SECRET]"
    )
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print("Error:", e)
