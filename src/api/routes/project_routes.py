from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from ..models.project import ProjectService
from engine_instance import design_engine

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects')
def projects():
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))
    projects = ProjectService.list_projects(user.username)
    return render_template('projects/project_manager.html', user=user, projects=projects)

@project_bp.route('/new-project', methods=['GET', 'POST'])
def new_project():
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))

    if request.method == 'POST':
        # Create a new project using service
        description = request.form.get('description')
        project_id = ProjectService.create_project(user.username, description)
        return redirect(url_for('project.project_details', username=user.username, project_id=project_id))

    # GET – just show the "new project" form
    return render_template('projects/new_project.html', user=user)

@project_bp.route('/project/<username>/<project_id>')
def project_details(username, project_id):
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))
    project_data = ProjectService.get_project_with_contexts(int(project_id), user.username)
    if not project_data:
        flash('Project not found', 'error')
        return redirect(url_for('project.projects'))
    return render_template('projects/project_dashboard.html', user=user, project=project_data)

@project_bp.route('/update-project/<username>/<int:project_id>', methods=['POST'])
def update_project(username, project_id):
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    user = design_engine.get_user(session_id)
    if not user or user.username != username:
        return redirect(url_for('user.login'))

    # In a full implementation you would validate changes and call a service.
    # For now simply flash success and redirect.
    flash('Project updated successfully', 'success')
    return redirect(url_for('project.project_details', username=username, project_id=project_id))

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
    context_id = ProjectService.add_context(project_id, context_text)
    return jsonify({'id': context_id, 'text': context_text})

@project_bp.route('/get-contexts/<int:project_id>')
def get_contexts(project_id):
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'Unauthorized'}), 401
    user = design_engine.get_user(session_id)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    # Placeholder – in production call ProjectService to fetch contexts.
    return jsonify({'project': 'ok', 'contexts': []})

@project_bp.route('/update-context/<int:context_id>', methods=['POST'])
def update_context(context_id):
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'Unauthorized'}), 401
    user = design_engine.get_user(session_id)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Text content required'}), 400
    new_text = data['text']
    if not new_text.strip():
        return jsonify({'error': 'Context text cannot be empty'}), 400
    # Placeholder – call a service to persist the update.
    return jsonify({'success': True, 'id': context_id, 'text': new_text})