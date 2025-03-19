from flask import Blueprint, render_template

# Define the blueprint for the example route
example_bp = Blueprint('example', __name__)

@example_bp.route('/routed-example-page')
def example_page():
    return render_template('example.html')
