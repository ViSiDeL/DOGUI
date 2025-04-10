from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pymysql
import json
from engine_instance import design_engine

project_bp = Blueprint('project', __name__)

# loading db config
def load_db_config():
    with open('config/db_connection.json') as config_file:
        return json.load(config_file)

# project page
@project_bp.route('/projects')
def projects():
    # redirect to login if not logged in
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))

    db_config = load_db_config()
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=int(db_config['port'])
        )
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT projectName, description, ID FROM projects WHERE username = %s",
                (user.username,)
            )
            projects = cursor.fetchall()
            
        return render_template('design/project_manager.html', user=user, projects=projects)
        
    except Exception as e:
        flash('Error loading projects', 'error')
        return render_template('design/project_manager.html', user=user, projects=[])
    
    finally:
        if 'connection' in locals():
            connection.close()

# create new project, go to project details page
@project_bp.route('/new-project')
def new_project():
    # redirect to login if not logged in
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))

    db_config = load_db_config()

    # make new project
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=int(db_config['port'])
        )
        
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO projects (username) VALUES (%s)",
                (user.username)
            )
            project_id = cursor.lastrowid
            connection.commit()
            
        return redirect(url_for('project.project_details', 
                            username=user.username, 
                            project_id=project_id))
        
    except Exception as e:
        flash('Error creating project', 'error')
        return redirect(url_for('project.projects'))
    
    finally:
        if 'connection' in locals():
            connection.close()

@project_bp.route('/project/<username>/<project_id>')
def project_details(username, project_id):
    # redirect to login if not logged in
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))
    
    # get project from db
    db_config = load_db_config()
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=int(db_config['port'])
        )
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT projectname, description, phase FROM projects WHERE id = %s AND username = %s",
                (project_id, username)
            )
            project = cursor.fetchone()
            
            if not project:
                flash('Project not found', 'error')
                return redirect(url_for('project.projects'))
            
            return render_template(
                'design/project_dashboard.html',
                user=user,
                project={
                    'id': project_id,
                    'name': project[0],
                    'description': project[1],
                    'phase': project[2]
                }
            )
            
    except Exception as e:
        flash('Error loading project', 'error')
        return redirect(url_for('project.projects'))
    finally:
        if 'connection' in locals():
            connection.close()

# project updates
@project_bp.route('/update-project/<username>/<int:project_id>', methods=['POST'])
def update_project(username, project_id):
    pass