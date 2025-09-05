import pymysql

try:
    conn = pymysql.connect(
        host="[REMOVEDSECRET]",
        user="[REMOVEDSECRET]",
        password="[REMOVEDSECRET]",
        port="[REMOVEDSECRET]",
        database="[REMOVEDSECRET]"
    )
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print("Error:", e)
