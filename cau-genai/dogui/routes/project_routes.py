from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import mysql.connector
import json
from engine_instance import design_engine

project_bp = Blueprint('project', __name__)

# loading db config
def load_db_config():
    with open('config/db_connection.json') as config_file:
        return json.load(config_file)

# registration page
@project_bp.route('/projects')
def projects():
    session_id = session.get('session_id')
    if session_id:
        user = design_engine.get_user(session_id)
        if user:
            return render_template('design/project_manager.html', user=user)
    
    # redirect to login if no active session
    return redirect(url_for('user.login'))