def create_app():
    from flask import Flask
    app = Flask(__name__, static_folder="../../dogui/static", template_folder="../../dogui/templates")
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
    from api.routes.user_routes import user_bp
    from api.routes.ai_routes import ai_bp
    from api.routes.test_routes import test_bp
    from api.routes.project_routes import project_bp
    from api.routes.asset_routes import asset_bp
    for bp in (user_bp, ai_bp, test_bp, project_bp, asset_bp):
        app.register_blueprint(bp)
    return app