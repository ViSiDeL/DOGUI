""" DOGUI flask application """
from flask import Flask, render_template, send_from_directory, g, redirect, url_for
import os
import random

# ROUTES
from api.routes.user_routes import user_bp
from api.routes.ai_routes import ai_bp
from api.routes.project_routes import project_bp
from api.routes.asset_routes import asset_bp

# DOGUI CLASS IMPORTS
from api.engine_instance import design_engine
from api.models.session import login_required

""" SETUP """

DOGUI_SITE_PATH = os.path.join(os.path.dirname(__file__), '..', 'dogui')
TEMPLATE_PATH = os.path.join(DOGUI_SITE_PATH, 'templates')
STATIC_PATH = os.path.join(DOGUI_SITE_PATH, 'static')
app = Flask(__name__, template_folder=TEMPLATE_PATH, static_folder=STATIC_PATH)

# for session management
app.config['SECRET_KEY'] = os.urandom(24)

# register blueprints for other routes
app.register_blueprint(user_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(project_bp)
app.register_blueprint(asset_bp)


""" ------------------ ROUTES ------------------ """

# /home or /
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
@login_required
def dashboard():
    user = g.user
    if user:
        return render_template('dashboard.html', user=user)
    return redirect(url_for('user.login'))


# handles node modules - needed for Flask apps with node js libs
@app.route('/node_modules/<path:filename>')
def node_modules(filename):
    return send_from_directory(os.path.join(app.root_path, 'node_modules'), filename)

# run - launches application
if __name__ == '__main__':
    app.run(debug=True, port=4242)
