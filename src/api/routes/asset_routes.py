from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, g
from api.models.asset import AssetService, _allowed_type
from src.api.models.session import login_required
import os

asset_bp = Blueprint('asset', __name__, url_prefix='/assets')

@asset_bp.route('/')
@login_required
def assets():
    user = g.user
    assets = AssetService.list_user_assets(user.username)
    return render_template('assets/assets.html', user=user, assets=assets)

@asset_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_asset():
    user = g.user
    return render_template('assets/new_asset.html', user=user)

@asset_bp.route('/upload/<asset_type>', methods=['GET', 'POST'])
@login_required
def upload_asset(asset_type):
    user = g.user
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)

        if file and _allowed_type(file.filename, asset_type):
            asset_name = request.form.get('asset_name', file.filename.rsplit('.', 1)[0])
            is_public = 'is_public' in request.form

            upload_id = AssetService.upload_asset(
                asset_type=asset_type,
                file_obj=file,
                asset_name=asset_name,
                is_public=is_public,
                user_id=user.user_id if not is_public else None,
            )
            flash('Asset uploaded successfully!', 'success')
            return redirect(url_for('asset.assets'))

    return render_template('assets/upload_asset.html', user=user, asset_type=asset_type)

@asset_bp.route('/download/<asset_type>/<filename>')
@login_required
def download_asset(asset_type, filename):
    download_url = AssetService.get_download_url(filename, asset_type)
    return redirect(download_url)

@asset_bp.route('/generate-model')
@login_required
def generate_model():
    user = g.user
    return render_template('assets/generate_model.html', user=user)

@asset_bp.route('/generate', methods=['POST'])
@login_required
def generate():
    # Placeholder – in production you would call a model generation service.
    return jsonify({'code': '// placeholder generated code', 'status': 'success'})

@asset_bp.route('/project/<int:project_id>/add-asset/<int:asset_id>', methods=['POST'])
@login_required
def add_asset_to_project(project_id, asset_id):
    AssetService.add_asset_to_project(project_id, asset_id)
    return jsonify({'status': 'success', 'message': 'Asset added to project'})

@asset_bp.route('/cad-assist')
@login_required
def cad_assist():
    user = g.user
    return render_template('assets/cad_assist.html', user=user)
