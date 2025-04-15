from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from ai_interface import call_ai_model, save_script_to_file, clean_response
import os
import scripts.generated_script as script


# Point to the templates/ directory where your HTML file is stored
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/ai/run-script', methods=['POST'])
def run_script():
    try:
        instance = script.initialize_autocad()
        script.draw_square(instance)
        script.save_drawing(instance)

        return jsonify({
            "message": "✅ CAD design generated and saved successfully!"
        }), 200

    except Exception as e:
        print(f"❌ Error while executing CAD script: {str(e)}")
        return jsonify({
            "message": f"❌ Failed to generate CAD design: {str(e)}"
        }), 500

# Route to serve your frontend page
@app.route('/')
def serve_html():
    return render_template('cad.html')

# API route for chatting with the AI
@app.route('/api/ai/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({'response': 'No prompt provided.'}), 400

    response = call_ai_model(prompt)
    clean = clean_response(response)

    if "def" in clean and "import" in clean:
        save_script_to_file(clean)

    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

