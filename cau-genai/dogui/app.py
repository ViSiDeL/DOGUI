from flask import Flask, render_template, send_from_directory
from routes.example_routes import example_bp
import os

app = Flask(__name__)

# Register blueprints for modular routing
app.register_blueprint(example_bp)

# Define a route
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# Serve node_modules
@app.route('/node_modules/<path:filename>')
def node_modules(filename):
    return send_from_directory(os.path.join(app.root_path, 'node_modules'), filename)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
