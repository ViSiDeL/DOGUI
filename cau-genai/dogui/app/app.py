from flask import Flask, render_template
from models.examples.ex_classes.example_class import ExampleClass
from routes.example_routes import example_bp

app = Flask(__name__)

# Register blueprints for modular routing
app.register_blueprint(example_bp)

# Define a route
@app.route('/')
def home():
    return "Hello, Flask!"

# Example route using the ExampleClass
@app.route('/example')
def example():
    example_instance = ExampleClass("Test Name")
    return f"ExampleClass says: {example_instance.name}"

# Example route with parameters
@app.route('/greet/<name>')
def greet(name):
    return render_template('greet.html', name=name)

# Example route to load a HTML file
@app.route('/example-page')
def example_page():
    return render_template('example.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
