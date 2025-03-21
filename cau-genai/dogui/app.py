from flask import Flask, render_template, send_from_directory
from routes.example_routes import example_bp
import os

app = Flask(__name__)

# register blueprints for other routes
app.register_blueprint(example_bp)

# home route - handles navigation to home page via /home or / (default)
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# handles node modules - needed for Flask apps with node js libs
@app.route('/node_modules/<path:filename>')
def node_modules(filename):
    return send_from_directory(os.path.join(app.root_path, 'node_modules'), filename)

# run - launches application
if __name__ == '__main__':
    app.run(debug=True)
