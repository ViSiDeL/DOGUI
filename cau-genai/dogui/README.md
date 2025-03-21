# dogui

A Flask-based web application with Node.js integration.

##  **Installation & Setup**

### **Prerequisites**
Ensure you have the following installed:
- [Python 3.11](https://www.python.org/downloads/) (comes by default with Microsoft Store installations)
- [Node.js](https://nodejs.org/) (includes `npm`)

### **1. Clone the Repository**
First, clone the repository from GitHub:
```bash
git clone <your-repo-url>

# cd into the dogui folder
cd cau-genai/dogui
```

### **2. Create and Activate a Virtual Environment**
It's recommended to use a virtual environment to keep dependencies isolated.
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

If you run into an error stating that Permission is denied, run the following command: 
```bash

# to fix the System.UnauthorizedAccessException,Microsoft.PowerShell.Commands.SetExecutionPolicyCommand error
Set-ExecutionPolicy -ExecutionPolicy AllSigned -Scope CurrentUser

# then activate source
source venv/bin/activate
```

### **3. Install Python Dependencies**
Install the Python dependencies into the virtual environment:
```bash
pip install -r requirements.txt
```

### **4. Install Node.js Dependencies**
Install the Node.js modules listed in package.json:
```bash
npm install
```

This will generate a node_modules folder if it doesn’t already exist.

### **5. Run the Flask Application**
Start the Flask server by running:

```bash
python app.py
```
The server will start on http://127.0.0.1:5000.

### **6. Access the Application**
Open your browser and visit:

```bash
http://127.0.0.1:5000
```

### **Project Structure**

```
plaintext
dogui/
 ├── app/
 │    ├── config/          # Configuration files
 │    ├── models/          # Database models
 │    ├── node_modules/    # Node.js dependencies
 │    ├── routes/          # Flask routes
 │    ├── static/          # Static assets (CSS, JS, images)
 │    ├── templates/       # HTML templates
 │    ├── app.py           # Flask app entry point
 │    ├── package.json     # Node.js dependencies
 │    ├── package-lock.json # Node.js lockfile
 │    └── tests/           # Unit tests
 ├── README.md
 ├── requirements.txt      # Python dependencies
```
### **Tips**
If you add new Python packages, update requirements.txt:
```bash
pip freeze > requirements.txt
```
To add new Node modules, use:
```bash
npm install <module-name> --save
```
