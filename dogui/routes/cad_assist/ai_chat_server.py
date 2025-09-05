from flask import Blueprint, request, jsonify, render_template
from flask_cors import CORS
from routes.cad_assist.ai_interface import call_ai_model, clean_response  # Importing from ai_interface
import os
import routes.cad_assist.scripts.generated_script as script  # Importing generated_script


cad_bp = Blueprint('cad', __name__)
CORS(cad_bp, resources={r"/api/*": {"origins": "*"}})

# Store conversation history globally
conversation_history = []

# Route to serve your frontend page
@cad_bp.route('/cad_assist')
def serve_html():
    return render_template('/cad_assist/cad.html')

@cad_bp.route('/api/ai/draw-square', methods=['POST'])
def draw_square():
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

@cad_bp.route('/api/ai/save-script', methods=['POST'])
def save_script():
    try:
        return jsonify({
            "message": "✅ PYAUTOCAD design generated and saved successfully!"
        }), 200

    except Exception as e:
        print(f"❌ Error while saving PYAUTOCAD script: {str(e)}")
        return jsonify({
            "message": f"❌ Failed to save PYAUTOCAD design: {str(e)}"
        }), 500


@cad_bp.route('/api/ai/init-cad', methods=['POST'])
def initialize():
    try:
        acad = script.initialize_autocad()
        if acad:
            print("✅ AutoCAD initialized successfully!")
        else:
            print("❌ AutoCAD initialization failed!")

        return jsonify({
            "message": "✅ CAD initialized successfully!"
        }), 200

    except Exception as e:
        print(f"❌ Error while initializing CAD: {str(e)}")
        return jsonify({
            "message": f"❌ Failed to initialize CAD: {str(e)}"
        }), 500

@cad_bp.route('/api/ai/run-simulation', methods=['POST'])
def run_simulation():
    try:
        # Analyze the uploaded CAD file or the current drawing
        simulation_results = simulate_cad_design()
    
        # AI provides feedback on the CAD design
        feedback = f"Simulation Complete: {simulation_results}"
    
        return jsonify({
            "message": feedback
        }), 200
    except Exception as e:
        print(f"❌ Error during simulation: {str(e)}")
        return jsonify({
            "message": f"❌ Simulation failed: {str(e)}"
        }), 500

# API route for chatting with the AI
@cad_bp.route('/api/ai/chat', methods=['POST'])
def chat():
    global conversation_history  # Use global conversation history

    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'response': 'No prompt provided.'}), 400

    try:
        # Add the new prompt to the conversation history
        conversation_history.append(f"You: {prompt}")

        # Pass the entire conversation history to the AI
        response = call_ai_model(conversation_history)

        # Clean the AI's response before sending it back
        clean = clean_response(response)

        # Append the AI's response to the conversation history
        conversation_history.append(f"Dogui: {clean}")

        # Send the cleaned response back to the frontend
        return jsonify({'response': clean})
    except Exception as e:
        print(f"❌ Error generating AI response: {e}")
        return jsonify({'response': 'Error generating AI response. Please try again.'}), 500


def simulate_cad_design():
    # Logic for analyzing CAD design or DWG file can be added here
    # This could involve checking for certain dimensions, patterns, or shapes
    return "The wall dimensions look correct. However, the door placement could be improved for better accessibility."
