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
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Get project info
            cursor.execute(
                """SELECT p.*, 
                GROUP_CONCAT(c.context_id, '|||', c.context_text SEPARATOR ';;;') AS contexts_data
                FROM projects p
                LEFT JOIN contexts c ON p.ID = c.project_id
                WHERE p.ID = %s AND p.username = %s
                GROUP BY p.ID""",
                (project_id, username)
            )
            project_data = cursor.fetchone()
            
            if not project_data:
                flash('Project not found', 'error')
                return redirect(url_for('project.projects'))
            
            # Parse contexts
            contexts = []
            if project_data['contexts_data']:
                for item in project_data['contexts_data'].split(';;;'):
                    context_id, text = item.split('|||')
                    contexts.append({
                        'id': int(context_id),
                        'text': text
                    })
            
            project = {
                'id': project_data['ID'],
                'name': project_data['projectName'],
                'description': project_data['description'],
                'phase': project_data['phase'],
                'init': project_data['init'],
                'created_at': project_data['created_at'],
                'last_edited': project_data['last_edited'],
                'contexts': contexts
            }
            
            return render_template(
                'projects/project_dashboard.html',
                user=user,
                project=project
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



""" ------------------------------ CONTEXT ------------------------------ """
@project_bp.route('/add-context/<int:project_id>', methods=['POST'])
def add_context(project_id):
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = design_engine.get_user(session_id)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    context_text = request.form.get('context')
    if not context_text:
        return jsonify({'error': 'Context text required'}), 400
    
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
            # Verify user owns the project
            cursor.execute(
                "SELECT 1 FROM projects WHERE ID = %s AND username = %s",
                (project_id, user.username)
            )
            if not cursor.fetchone():
                return jsonify({'error': 'Project not found'}), 404
            
            # Add context
            cursor.execute(
                "INSERT INTO contexts (project_id, context_text) VALUES (%s, %s)",
                (project_id, context_text)
            )
            context_id = cursor.lastrowid
            connection.commit()
            
            return jsonify({
                'id': context_id,
                'text': context_text
            })
        
    except Exception as e:
        print(f"Error adding context: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        if 'connection' in locals():
            connection.close()

@project_bp.route('/get-contexts/<int:project_id>')
def get_contexts(project_id):
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = design_engine.get_user(session_id)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    db_config = load_db_config()
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=int(db_config['port'])
        )
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # get project info
            cursor.execute(
                "SELECT projectName, description FROM projects WHERE ID = %s AND username = %s",
                (project_id, user.username)
            )
            project = cursor.fetchone()
            
            if not project:
                return jsonify({'error': 'Project not found'}), 404
            
            # get contexts
            cursor.execute(
                "SELECT context_text FROM contexts WHERE project_id = %s ORDER BY created_at DESC",
                (project_id,)
            )
            contexts = cursor.fetchall()
            
            return jsonify({
                'project': project,
                'contexts': [c['context_text'] for c in contexts]
            })
            
    except Exception as e:
        print(f"Error getting contexts: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        if 'connection' in locals():
            connection.close()

@project_bp.route('/update-context/<int:context_id>', methods=['POST'])
def update_context(context_id):
    # Authentication check
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = design_engine.get_user(session_id)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Get updated text from JSON request body
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Text content required'}), 400
    
    new_text = data['text']
    if not new_text.strip():
        return jsonify({'error': 'Context text cannot be empty'}), 400
    
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
            # Verify user owns the context (through project ownership)
            cursor.execute(
                """SELECT 1 FROM contexts c
                JOIN projects p ON c.project_id = p.ID
                WHERE c.context_id = %s AND p.username = %s""",
                (context_id, user.username)
            )
            if not cursor.fetchone():
                return jsonify({'error': 'Context not found'}), 404
            
            # Update context
            cursor.execute(
                "UPDATE contexts SET context_text = %s WHERE context_id = %s",
                (new_text, context_id)
            )
            connection.commit()
            
            return jsonify({
                'success': True,
                'id': context_id,
                'text': new_text
            })
            
    except Exception as e:
        print(f"Error updating context: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        if 'connection' in locals():
            connection.close()