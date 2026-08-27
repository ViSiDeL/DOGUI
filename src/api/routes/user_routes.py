from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from api.models.auth import AuthService
from api.engine_instance import design_engine

user_bp = Blueprint('user', __name__)
DEFAULT_ROLE = "Engineer"

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # register 
        user_id = AuthService.register(username, password)

        # login if successful
        session['session_id'] = str(user_id)
        flash('User registered successfully!', 'success')
        print(f"User '{username}' (ID: {user_id}) has registered.")
        return redirect(url_for('dashboard'))
    return render_template('accounts/register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = AuthService.login(username, password)
        if user_id:
            session['session_id'] = str(user_id)
            user_info = AuthService.get_user_info(user_id)
            if user_info:
                db_username, db_role = user_info
            else:
                db_username, db_role = username, "Engineer"
            design_engine.add_user(session['session_id'], user_id, db_username, db_role)
            flash('Login successful!', 'success')
            print(f"User '{db_username}' (ID: {user_id}) has logged in.")
            return redirect(url_for('dashboard'))
        else:
            flash('invalid username or password!', 'danger')
    return render_template('accounts/login.html')

@user_bp.route('/logout')
def logout():
    session_id = session.get('session_id')
    if session_id:
        AuthService.logout(int(session_id))
        session.pop('session_id', None)
        flash('You have been logged out.', 'success')
    return redirect(url_for('user.login'))
