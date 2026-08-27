from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, g
from api.models.project import ProjectService
from api.models.inference import generate_text
from src.api.models.session import login_required

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects')
@login_required
def projects():
    user = g.user
    projects = ProjectService.list_projects(user.username)
    return render_template('projects/project_manager.html', user=user, projects=projects)

@project_bp.route('/new-project')
@login_required
def new_project():
    user = g.user
    project_id = ProjectService.create_project(user.username, description="")
    return redirect(url_for('project.project_details', username=user.username, project_id=project_id))

@project_bp.route('/project/<username>/<project_id>')
@login_required
def project_details(username, project_id):
    user = g.user
    project_data = ProjectService.get_project_with_contexts(int(project_id), user.username)
    if not project_data:
        flash('Project not found', 'error')
        return redirect(url_for('project.projects'))
    return render_template('projects/project_dashboard.html', user=user, project=project_data)

@project_bp.route('/update-project/<username>/<int:project_id>', methods=['POST'])
@login_required
def update_project(username, project_id):
    user = g.user
    if user.username != username:
        return redirect(url_for('user.login'))

    # first-time init or explicit "regenerate name" both (re)generate a name from the description
    is_naming_action = 'description' in request.form and (
        'init' in request.form or 'regen' in request.form
    )

    updates = {}

    if is_naming_action:
        description = request.form['description'].strip()
        if not description:
            flash('Description cannot be empty', 'error')
            return redirect(url_for('project.project_details', username=username, project_id=project_id))

        prompt = f"""
        Generate a concise, professional project name (2-4 words max) based on this description:
        "{description}"

        Respond ONLY with the project name, no additional text or explanations.
        Try to make the name trendy, unique, but still short and descriptive. You can add spaces if necessary.
        Project Name:
        """

        try:
            project_name = generate_text(prompt=prompt).strip().strip('"').strip("'")
            if not project_name:
                project_name = f"Project {project_id}"
        except Exception as e:
            print(f"Error generating project name: {e}")
            project_name = f"Project {project_id}"

        updates.update({
            'project_name': project_name,
            'description': description,
            'phase': 'ideation',
            'init': 1,
        })
        flash('Project initialized successfully!', 'success')
    else:
        if 'name' in request.form and request.form['name'].strip():
            updates['project_name'] = request.form['name'].strip()
        if 'description' in request.form and request.form['description'].strip():
            updates['description'] = request.form['description'].strip()
        if 'phase' in request.form:
            updates['phase'] = request.form['phase']
        if 'init' in request.form and request.form['init'].strip():
            updates['init'] = int(request.form['init'])

        if not updates:
            flash('No changes detected', 'info')
            return redirect(url_for('project.project_details', username=username, project_id=project_id))

    success = ProjectService.update_project(
        project_id=project_id,
        username=username,
        **updates
    )

    if not success:
        flash('Error updating project or you are not authorized.', 'error')
    elif not is_naming_action:
        flash('Project updated successfully', 'success')

    return redirect(url_for('project.project_details', username=username, project_id=project_id))

@project_bp.route('/add-context/<int:project_id>', methods=['POST'])
@login_required
def add_context(project_id):
    context_text = request.form.get('context')
    if not context_text:
        return jsonify({'error': 'Context text required'}), 400
    context_id = ProjectService.add_context(project_id, context_text)
    return jsonify({'id': context_id, 'text': context_text})

@project_bp.route('/get-contexts/<int:project_id>')
@login_required
def get_contexts(project_id):
    user = g.user
    try:
        contexts = ProjectService.get_contexts(project_id, user.username)
        if not contexts:
            return jsonify({'error': 'No contexts found'}), 404
        return jsonify({'contexts': contexts})
    except Exception as e:
        print(f"Error getting contexts: {e}")
        return jsonify({'error': 'Database error'}), 500

@project_bp.route('/update-context/<int:context_id>', methods=['POST'])
@login_required
def update_context(context_id):
    user = g.user

    # verify ownership of context
    if not ProjectService.is_context_owned(context_id, user.username):
        return jsonify({'error': 'Context not found or not owned'}), 403

    # new text
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Text content required'}), 400
    new_text = data['text']
    if not new_text.strip():
        return jsonify({'error': 'Context text cannot be empty'}), 400
    success = ProjectService.update_context(context_id, new_text)
    if not success:
        return jsonify({'error': 'Failed to update context'}), 500
    return jsonify({'success': True, 'id': context_id, 'text': new_text})
