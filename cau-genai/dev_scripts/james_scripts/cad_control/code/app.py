from flask import Flask, render_template, request, jsonify
from watson_connector import WatsonConnector
from controllers.cad_controller import CADController
from input_processor import InputProcessor

app = Flask(__name__)

watson = WatsonConnector()
cad = CADController()
processor = InputProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    input_type, processed_input = processor.process_input(user_input)

    if input_type == "CAD":
        response = cad.execute_command(processed_input)
    else:
        response = watson.get_response(processed_input)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
