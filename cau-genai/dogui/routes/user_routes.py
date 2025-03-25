from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
import json

user_bp = Blueprint('user', __name__)

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
        
        # connect to database using config
        db_config = load_db_config()
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=db_config['port']
        )
        cursor = connection.cursor()
        
        # check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('user.register'))
        
        # insert new user
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        cursor.close()
        connection.close()
        
        flash('User registered successfully!', 'success')
        return redirect(url_for('user.login'))
    
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
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=db_config['port']
        )
        cursor = connection.cursor()
        
        # check if username and password match
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()

        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('user.login'))
    
    return render_template('accounts/login.html')


# login page        
@user_bp.route('/logout', methods=['GET'])
def logout():
    # TODO, implement proper logout functionalities
    return render_template('accounts/login.html')
