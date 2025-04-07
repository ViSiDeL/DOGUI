from flask import Flask, render_template, send_from_directory, jsonify, request
import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(__name__)

credentials = Credentials(
    url = "https://us-south.ml.cloud.ibm.com",
    api_key = "APIKEY"
)
model_id = "ibm/granite-8b-code-instruct"

model = ModelInference(
    model_id=model_id,
    credentials=credentials,
    project_id="[SECRET]",
    params= {
		"decoding_method": "greedy",
		"max_new_tokens": 500,
		"min_new_tokens": 0,
		"repetition_penalty": 1
	},
)

def clean_generated_code(raw_code):
    # raw_code = raw_code.split('\n\n')[0]

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
        Here is their description "{user_description}"
        Respond with ONLY the three.js code the creates the objects and adds them to the scence. 
        limit size to about 10x10x10 units.
        Assume that parameters (scence, camera, renderer) are already provided.
        DO NOT include any intro, outro, explanations, comments, description or text outside the code. respond with ONLY code and no sentences.
        ONLY generate the code that creates and adds 3D objects to the scene with described materials, colors, position, etc..
        You can include multiple objects/shapes/meshes/geometry/color as necessary, try to result as close as possible to what the user wants.
        """
        #print(prompt)

        # generate code
        response = model.generate(prompt=prompt)
        #print(response['results'])
        
        # cleanup
        generated_code = clean_generated_code(response['results'][0]['generated_text'])

        # messages = [
        #     {"role": "system", "content": """
        #         You are a three.js generator, meant to generate the code needed to create a 3d model in three.js for a user based on a description of their engineering project in three.js.
        # Respond with ONLY the three.js code the creates the objects and adds them to the scence. 
        # limit size to about 10x10x10 units
        # Assume that parameters (scence, camera, renderer) are already provided.
        # DO NOT include any intro, outro, explanations, comments, description or text outside the code. respond with ONLY code and no sentences.
        # DO NOT include any test cases or examples.
        # ONLY generate code that creates and adds 3D objects to the scene with described materials, colors, position, etc..
        # You can include multiple objects/shapes/meshes/geometry/color as necessary, try to result as close as possible to what the user wants
        # Your response should ONLY be the code, no other text.
        #     """},
        #     {"role": "user", "content": f"{user_description}"}
        # ]
        # generated_response = model.chat(messages=messages)

        # # Print all response
        # print(generated_response)

        # # Print only content
        # print(generated_response['choices'][0]['message']['content'])

        # generated_code = clean_generated_code(generated_response['choices'][0]['message']['content'])

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
