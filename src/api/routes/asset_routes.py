from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
import pymysql
import json
import os
import re
from engine_instance import design_engine
from werkzeug.utils import secure_filename
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
from dogui_modelgen.threejs_generator import generate_threejs_snippet


asset_bp = Blueprint('asset', __name__, url_prefix='/assets')

ALLOWED_EXTENSIONS = {
    'model': ['stl', 'obj', 'blend', 'gltf', 'glb'],
    'drawing': ['dwg', 'dxf', 'step', 'iges', 'blend'],
    'image': ['png', 'jpg', 'jpeg', 'gif']
}
def allowed_file(filename, asset_type):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[asset_type]

# loading db config
def load_db_config():
    with open('config/db_connection.json') as config_file:
        return json.load(config_file)
    
# loading watson apikey
def load_watson_config():
    with open('config/watson_info.json') as watson_config_file:
        return json.load(watson_config_file)
    
# watson setup
watson_config = load_watson_config() 
credentials = Credentials(
    url = watson_config['url'],
    api_key = watson_config['IBM_API_KEY']
)
gen_model = ModelInference(
    model_id=watson_config['model_id'],
    credentials=credentials,
    project_id=watson_config['project_id'],
    params= {
		"decoding_method": "greedy",
		"max_new_tokens": 900,
		"min_new_tokens": 0,
		"repetition_penalty": 1
	},
)

""" -------------------------------- ASSET MANAGEMENT -------------------------------- """

@asset_bp.route('/')
def assets():
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))
    
    db_config = load_db_config()
    # get user's assets and public assets
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=int(db_config['port'])
        )
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT asset_url, asset_type, asset_name, user_id 
                FROM assets 
                WHERE user_id = %s OR user_id IS NULL
                ORDER BY created_at DESC
            """, (user.user_id,))
            assets = cursor.fetchall()
            print(assets)
            
            return render_template(
                'assets/assets.html',
                user=user,
                assets=assets
            )
            
    except Exception as e:
        print(f"Error loading assets: {e}")
        return render_template('assets/assets.html', user=user, assets=[])
    
    finally:
        if 'connection' in locals():
            connection.close()

@asset_bp.route('/new', methods=['GET', 'POST'])
def new_asset():
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))
    
    if request.method == 'POST':
        print("starting new asset")
        asset_type = request.form.get('asset_type')
        creation_method = request.form.get('creation_method')
        
        # model creation creation method
        if asset_type == 'model' and not creation_method:
            return render_template('assets/model_creation_method.html', 
                                user=user,
                                asset_type=asset_type)
        
        if asset_type == 'drawing' and not creation_method:
            return render_template('assets/drawing_creation_method.html', 
                                user=user,
                                asset_type=asset_type)
        
        if creation_method == 'upload':
            return redirect(url_for('asset.upload_asset', asset_type=asset_type))
        elif creation_method == 'generate':
            return redirect(url_for('asset.generate_model'))
        elif creation_method == 'CAD':
            return redirect(url_for('asset.cad_assist'))
        
    return render_template('assets/new_asset.html', user=user)

@asset_bp.route('/upload/<asset_type>', methods=['GET', 'POST'])
def upload_asset(asset_type):
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))
    
    if request.method == 'POST':
        # file upload
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        print(file)
        print(allowed_file(file.filename, asset_type))

        if file and allowed_file(file.filename, asset_type):
            print("attempting to save file")
            filename = secure_filename(file.filename)
            asset_name = request.form.get('asset_name', filename.rsplit('.', 1)[0])
            is_public = 'is_public' in request.form
            
            # Save file
            upload_folder = os.path.join('static', 'assets', f"{asset_type}s")
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            print(f"file saved? at {filepath}")
            
            # Save to database
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
                        "INSERT INTO assets (asset_url, asset_type, asset_name, user_id) VALUES (%s, %s, %s, %s)",
                        (filename, asset_type, asset_name, None if is_public else user.user_id)
                    )
                    connection.commit()
                
                flash('Asset uploaded successfully!', 'success')
                return redirect(url_for('asset.assets'))
                
            except Exception as e:
                flash(f'Error saving asset: {str(e)}', 'error')
                print(f'Error saving asset: {str(e)}', 'error')
                return redirect(request.url)
            
            finally:
                if 'connection' in locals():
                    connection.close()
        else:
            flash('Invalid file type for selected asset type', 'error')
            return redirect(request.url)
    
    print('loaded upload page')
    return render_template('assets/upload_asset.html', user=user, asset_type=asset_type)

@asset_bp.route('/download/<asset_type>/<filename>')
def download_asset(asset_type, filename):
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))
    
    # Verify user has permission to download
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
                "SELECT 1 FROM assets WHERE asset_url = %s AND (user_id = %s OR user_id IS NULL)",
                (filename, user.user_id)
            )
            if not cursor.fetchone():
                flash('Asset not found or permission denied', 'error')
                return redirect(url_for('asset.assets'))
        
        # Serve the file
        directory = os.path.join('static', 'assets', f"{asset_type}s")
        return send_from_directory(
            directory=directory,
            path=filename,
            as_attachment=True
        )
        
    except Exception as e:
        flash(f'Error downloading asset: {str(e)}', 'error')
        print(f'Error downloading asset: {str(e)}', 'error')
        return redirect(url_for('asset.assets'))
    
    finally:
        if 'connection' in locals():
            connection.close()

""" -------------------------------- MODEL GENERATION -------------------------------- """

@asset_bp.route('/generate-model')
def generate_model():
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))
    
    return render_template('assets/generate_model.html', user=user)

@asset_bp.route('/generate', methods=['POST'])
def generate():
    try:
        user_description = request.json.get('description')
        code = generate_threejs_snippet(gen_model, user_description)
        return jsonify({'code': code, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@asset_bp.route('/project/<int:project_id>/add-asset/<int:asset_id>', methods=['POST'])
def add_asset_to_project(project_id, asset_id):
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
        
        with connection.cursor() as cursor:
            # verify user ownership
            cursor.execute(
                """SELECT 1 FROM projects p
                WHERE p.ID = %s AND p.username = %s""",
                (project_id, user.username)
            )
            if not cursor.fetchone():
                return jsonify({'error': 'Project not found'}), 404
            
            # verify user access
            cursor.execute(
                """SELECT 1 FROM assets 
                WHERE id = %s AND (user_id = %s OR user_id IS NULL)""",
                (asset_id, user.user_id)
            )
            if not cursor.fetchone():
                return jsonify({'error': 'Asset not found or unauthorized'}), 404
            
            # add association
            cursor.execute(
                "INSERT INTO project_assets (project_id, asset_id) VALUES (%s, %s)",
                (project_id, asset_id)
            )
            connection.commit()
            
            # get asset details
            cursor.execute(
                """SELECT a.id, a.asset_url, a.asset_name, a.asset_type 
                FROM assets a WHERE a.id = %s""",
                (asset_id,)
            )
            asset = cursor.fetchone()
            
            return jsonify({
                'id': asset[0],
                'filename': asset[1],
                'name': asset[2],
                'type': asset[3]
            })
            
    except pymysql.err.IntegrityError:
        return jsonify({'error': 'Asset already in project'}), 400
    except Exception as e:
        print(f"Error adding asset to project: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        if 'connection' in locals():
            connection.close()

@asset_bp.route('/cad-assist')
def cad_assist():
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))
    
    return render_template('assets/cad_assist.html', user=user)