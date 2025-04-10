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
                'design/assets.html',
                user=user,
                assets=assets
            )
            
    except Exception as e:
        print(f"Error loading assets: {e}")
        return render_template('design/assets.html', user=user, assets=[])
    
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
            return render_template('design/model_creation_method.html', 
                                user=user,
                                asset_type=asset_type)
        
        if creation_method == 'upload':
            return redirect(url_for('asset.upload_asset', asset_type=asset_type))
        elif creation_method == 'generate':
            return redirect(url_for('asset.generate_model'))
        
    return render_template('design/new_asset.html', user=user)

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
    return render_template('design/upload_asset.html', user=user, asset_type=asset_type)

@asset_bp.route('/generate-model')
def generate_model():
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('user.login'))
    
    user = design_engine.get_user(session_id)
    if not user:
        return redirect(url_for('user.login'))
    
    return render_template('design/generate_model.html', user=user)

def clean_generated_code(raw_code):
    unwanted_patterns = [
        r'var\s+scene\s*=\s*new\s+THREE\.Scene\(\);?',
        r'var\s+camera\s*=\s*new\s+THREE\.PerspectiveCamera\([^;]*\);?',
        r'var\s+renderer\s*=\s*new\s+THREE\.WebGLRenderer\([^;]*\);?',
        r'renderer\.setSize\([^;]*\);?',
        r'document\.body\.appendChild\([^;]*\);?',
        r'renderer\.render\([^;]*\);?',
    ]
    
    for pattern in unwanted_patterns:
        raw_code = re.sub(pattern, '', raw_code, flags=re.IGNORECASE)

    for marker in ['```javascript', '```', '[RESP]', '// THREE.JS CODE START', '// THREE.JS CODE END']:
        raw_code = raw_code.replace(marker, '')
    
    # whitespace and empty lines
    cleaned = '\n'.join(
        line.strip() 
        for line in raw_code.split('\n') 
        if line.strip() and not line.strip().startswith(('//', '/*', '*', '*/'))
    ).strip()
    
    # semicolons
    if not cleaned.endswith(';'):
        cleaned += ';'
    
    return cleaned

@asset_bp.route('/generate', methods=['POST'])
def generate():
    try:
        user_description = request.json.get('description')
        print(f"generating ({user_description}).......")
        
        # prompt for watson
        prompt = f"""
        You are a three.js generator, meant to generate the code needed to create a 3d model in three.js for a user based on a description of their engineering project in three.js.
        Here is their description "{user_description}". 
        try to result as close as possible to what the user wants.
        limit size to about 10x10x10 units. Use MeshStandardMaterial when relevant so the material will interact with the scene's lights.
        Include multiple objects/shapes/meshes/geometry/color as necessary.
        Assume that parameters (scence, camera, renderer) are already provided so do not define a new instance of any of these.
        DO NOT include any intro, outro, explanations, comments, description or text outside the code. respond with ONLY the three.js code the creates the objects and adds them to the scence.
        ONLY generate the code that creates and adds 3D objects to the scene with described materials, colors, position, etc..
        """
        #print(prompt)

        # generate code
        response = gen_model.generate(prompt=prompt)
        #print(response['results'])
        
        # cleanup
        generated_code = clean_generated_code(response['results'][0]['generated_text'])

        #print(generated_code)
        print(f"\nresponse:\n---------------\n{generated_code}\n---------------")
        
        return jsonify({'code': generated_code, 'status': 'success'})
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500