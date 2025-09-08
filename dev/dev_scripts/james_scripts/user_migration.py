import pymysql
import json
import os
from werkzeug.security import generate_password_hash

def load_db_config():
    config_path = os.path.join(os.path.dirname(__file__), 'db_connection.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"error: configuration file not found at {config_path}")
        return None

def hash_existing_passwords():
    print("starting password hashing migration...")
    
    db_config = load_db_config()
    if not db_config:
        return

    connection = None
    cursor = None
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=int(db_config['port']),
            autocommit=True # this is the key to fixing the hang
        )
        # use dictcursor to get data with column names
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # select all users from the database
        cursor.execute("SELECT id, password FROM users")
        users = cursor.fetchall()
        
        if not users:
            print("no users found in the database. migration complete.")
            return

        print(f"found {len(users)} users to process.")
        
        for user in users:
            user_id = user['id']
            # we check if the password looks like a hash already.
            # this prevents re-hashing if the script is run multiple times.
            if not user['password'].startswith('pbkdf2:sha256:'):
                current_password = user['password']
                # hash the plaintext password
                hashed_password = generate_password_hash(current_password)
                
                print(f"attempting to hash password for user with id {user_id}...")
                
                # update the user's password in the database
                update_query = "UPDATE users SET password = %s WHERE id = %s"
                cursor.execute(update_query, (hashed_password, user_id))
                
                # with autocommit=True, we don't need a separate commit call here
                print(f"user with id {user_id} password has been hashed and updated.")
            else:
                print(f"user with id {user_id} password is already hashed. skipping.")
        
        print("migration successful! all passwords are now hashed.")

    except pymysql.MySQLError as e:
        print(f"database error occurred: {e}")
        if connection:
            connection.rollback()
    except Exception as e:
        print(f"an unexpected error occurred: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("database connection closed.")

if __name__ == "__main__":
    # this ensures the function is called only when the script is executed directly
    hash_existing_passwords()
