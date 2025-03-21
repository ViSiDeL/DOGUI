from flask import Flask, render_template, send_from_directory
import os

from routes.user_routes import user_bp
from routes.ai_routes import ai_bp
from routes.test_routes import test_bp

app = Flask(__name__)

# creating secret key for session management
app.config['SECRET_KEY'] = os.urandom(24)

# register blueprints for other routes
app.register_blueprint(user_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(test_bp)

# home route - handles navigation to home page via /home or / (default)
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('design/dashboard.html')


# handles node modules - needed for Flask apps with node js libs
@app.route('/node_modules/<path:filename>')
def node_modules(filename):
    return send_from_directory(os.path.join(app.root_path, 'node_modules'), filename)

# run - launches application
if __name__ == '__main__':
    app.run(debug=True)
