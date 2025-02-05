from flask import Flask, render_template
app = Flask(__name__, template_folder='templates') #creates flash instance


#home/index
@app.route("/") #specifies path location once 
def home(): #function determines what it does when you go to specified path location
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)