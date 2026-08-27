"""
IMPORTS
"""


from flask import Flask, request, render_template, send_from_directory, session, redirect, url_for
import os
import random

# ROUTES
from src.api.routes.user_routes import user_bp
from src.api.routes.ai_routes import ai_bp
from src.api.routes.test_routes import test_bp
from src.api.routes.project_routes import project_bp
from src.api.routes.asset_routes import asset_bp

# DOGUI CLASS IMPORTS
from src.api.engine_instance import design_engine

"""
SETUP
"""

app = Flask(__name__)

# creating secret key for session management
app.config['SECRET_KEY'] = os.urandom(24)

# register blueprints for other routes
app.register_blueprint(user_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(test_bp)
app.register_blueprint(project_bp)
app.register_blueprint(asset_bp)

"""
------------------ METHODS/FUNCTIONS ------------------
"""


"""
------------------ STARTUP ROUTINE ------------------
"""


"""
------------------ ROUTES ------------------
"""

# home route - handles navigation to home page via /home or / (default)
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# spaceship
@app.route('/ship')
def ship():
    return render_template('/ship/ship.html')

# dashboard
@app.route('/dashboard')
def dashboard():
    session_id = session.get('session_id')
    if session_id:
        user = design_engine.get_user(session_id)
        if user:
            return render_template('dashboard.html', user=user)
    
    # redirect to login if no active session
    return redirect(url_for('user.login'))


# handles node modules - needed for Flask apps with node js libs
@app.route('/node_modules/<path:filename>')
def node_modules(filename):
    return send_from_directory(os.path.join(app.root_path, 'node_modules'), filename)

# run - launches application
if __name__ == '__main__':
    app.run(debug=True, port=4242)
