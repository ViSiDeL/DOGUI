from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import pymysql
import json
import requests
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
                "SELECT projectName, description, ID, phase, created_at, last_edited FROM projects WHERE username = %s",
                (user.username,)
            )
            projects = cursor.fetchall()
            #print(projects)
            
        return render_template('projects/project_manager.html', user=user, projects=projects)
        
    except Exception as e:
        flash('Error loading projects', 'error')
        print(f'Error loading projects {e}')
        return render_template('projects/project_manager.html', user=user, projects=[])
    
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
        print(f'Error creating project {e}')
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
                "SELECT projectname, description, phase, init, created_at, last_edited FROM projects WHERE id = %s AND username = %s",
                (project_id, username)
            )
            project = cursor.fetchone()
            
            if not project:
                flash('Project not found', 'error')
                return redirect(url_for('project.projects'))
            
            #print(project)
            
            return render_template(
                'projects/project_dashboard.html',
                user=user,
                project={
                    'id': project_id,
                    'name': project[0],
                    'description': project[1],
                    'phase': project[2],
                    'init': project[3], 
                    'created_at': project[4],
                    'last_edited': project[5]
                }
            )
            
    except Exception as e:
        flash('Error loading project', 'error')
        print(f'Error loading project {e}')
        return redirect(url_for('project.projects'))
    finally:
        if 'connection' in locals():
            connection.close()

# project updates
@project_bp.route('/update-project/<username>/<int:project_id>', methods=['POST'])
def update_project(username, project_id):
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    user = design_engine.get_user(session_id)
    if not user or user.username != username:
        return redirect(url_for('user.login'))

    db_config = load_db_config()
    try:
        #form_data = request.form
        #for key, value in form_data.items():
            #print(f"{key}: {value}")
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=int(db_config['port'])
        )
        
        with connection.cursor() as cursor:
            # select project data
            cursor.execute(
                "SELECT init, projectName, description FROM projects WHERE id = %s AND username = %s",
                (project_id, username)
            )
            project = cursor.fetchone()
            
            if not project:
                flash('Project not found', 'error')
                return redirect(url_for('project.projects'))
            
            #print(project)

            current_init = project[0]
            updates = {}
            params = []
            
            #print(current_init)
            # project initialization
            if (current_init == 0 or 'regen' in request.form) and 'description' in request.form:
                description = request.form['description']
                if not description:
                    flash('Description cannot be empty', 'error')
                    return redirect(url_for('project.project_details', 
                                        username=username, 
                                        project_id=project_id))
                
                # generate project name
                try:
                    response = requests.post(
                        'http://localhost:5000/generate-project-name',
                        json={'description': description},
                        headers={'Content-Type': 'application/json'}
                    )
                    project_name = response.json().get('project_name', f"Project {project_id}")
                except Exception as e:
                    print(f"Error generating name: {e}")
                    project_name = f"Project {project_id}"
                
                updates.update({
                    'projectName': project_name,
                    'description': description,
                    'phase': 'ideation',
                    'init': True
                })
                flash('Project initialized successfully!', 'success')
            
            # regular updates
            else:
                if 'name' in request.form:
                    updates['projectName'] = request.form['name']
                if 'description' in request.form:
                    updates['description'] = request.form['description']
                if 'phase' in request.form:
                    updates['phase'] = request.form['phase']
                
                #print(updates)

                if not updates:
                    flash('No changes detected', 'info')
                    print("no updates")
                    return redirect(url_for('project.project_details', 
                                        username=username, 
                                        project_id=project_id))
                
                flash('Project updated successfully', 'success')
            
            # execute update query
            if updates:
                set_clause = ', '.join([f"{k} = %s" for k in updates])
                query = f"UPDATE projects SET {set_clause} WHERE id = %s AND username = %s"
                params = list(updates.values()) + [project_id, username]
                
                cursor.execute(query, params)
                connection.commit()
            
        return redirect(url_for('project.project_details', 
                            username=username, 
                            project_id=project_id))
            
    except Exception as e:
        print(f"Error updating project: {e}")
        flash('Error updating project', 'error')
        return redirect(url_for('project.project_details', 
                            username=username, 
                            project_id=project_id))
    finally:
        if 'connection' in locals():
            connection.close()