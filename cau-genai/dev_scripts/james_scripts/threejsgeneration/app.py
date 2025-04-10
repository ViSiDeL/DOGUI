from flask import Flask, render_template, send_from_directory, jsonify, request
import os, re
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv() 
credentials = Credentials(
    url = "https://us-south.ml.cloud.ibm.com",
    api_key = os.getenv("IBM_API_KEY")
)
model_id = "ibm/granite-8b-code-instruct"

model = ModelInference(
    model_id=model_id,
    credentials=credentials,
    project_id="8d70c9a1-49ae-4848-81e4-0d1c34fc320a",
    params= {
		"decoding_method": "greedy",
		"max_new_tokens": 900,
		"min_new_tokens": 0,
		"repetition_penalty": 1
	},
)

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
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
        print(prompt)

        # generate code
        response = model.generate(prompt=prompt)
        #print(response['results'])
        
        # cleanup
        generated_code = clean_generated_code(response['results'][0]['generated_text'])

        #print(generated_code)
        print(f"\nresponse:\n---------------\n{generated_code}\n---------------")
        
        return jsonify({'code': generated_code, 'status': 'success'})
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500


# handles node modules - needed for Flask apps with node js libs
@app.route('/node_modules/<path:filename>')
def node_modules(filename):
    return send_from_directory(os.path.join(app.root_path, 'node_modules'), filename)

# run - launches application
if __name__ == '__main__':
    app.run(debug=True)
