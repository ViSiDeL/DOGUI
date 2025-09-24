from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pymysql
import json
from models.user import User
from engine_instance import design_engine
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user', __name__)
DEFAULT_ROLE = "Engineer"

# loading db config
def load_db_config():
    with open('config/db_connection.json') as config_file:
        return json.load(config_file)

# registration page
@user_bp.route('/register', methods=['GET', 'POST'])
def register():

    # registering (POST)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # pass hashing
        hashed_password = generate_password_hash(password)

        # connect to database using config
        db_config = load_db_config()
        connection = None
        cursor = None
        try:
            connection = pymysql.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
                port=int(db_config['port'])
            )
            cursor = connection.cursor()
            
            # check if the username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                flash('Username already exists!', 'danger')
                return redirect(url_for('user.register'))
            
            # insert new user
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            connection.commit()

            # finish
            flash('User registered successfully!', 'success')

            # get user id
            user_id = cursor.lastrowid

            # log in
            session['session_id'] = str(user_id)
            design_engine.add_user(session['session_id'], user_id=user_id, username=username, role=DEFAULT_ROLE)
            flash('Login successful!', 'success')
            print(f"User '{username}' (ID: {user_id}) has logged in.")
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
            print(f'An error occurred: {e}')
            if connection:
                connection.rollback()
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    return render_template('accounts/register.html')

# login page
@user_bp.route('/login', methods=['GET', 'POST'])
def login():

    # logging in (POST)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # connect to database using config
        db_config = load_db_config()
        connection = None
        cursor = None
        try:
            connection = pymysql.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
                port=int(db_config['port'])
            )
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # find the user by username
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                user_id = user['id']
                username = user['username']

                # check against stored hash
                if check_password_hash(user['password'], password):
                    # log in
                    session['session_id'] = str(user_id)
                    design_engine.add_user(session['session_id'], user_id=user_id, username=username, role=DEFAULT_ROLE)
                    flash('Login successful!', 'success')
                    print(f"User '{username}' (ID: {user_id}) has logged in.")
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid username or password!', 'danger')
            else:
                flash('Invalid username or password!', 'danger')
    
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
            print(f'An error occurred: {e}')
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    return render_template('accounts/login.html')


# login page        
@user_bp.route('/logout', methods=['GET'])
def logout():
    session_id = session.get('session_id')
    
    if session_id:
        design_engine.remove_user(session_id)
        session.pop('session_id', None)
        flash('You have been logged out.', 'success')

    return redirect(url_for('user.login'))
