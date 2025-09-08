# dogui

Follow the instructions below to install a local version of DOGUI.

## **Installation & Setup**

### **Prerequisites**

Ensure you have the following:

- [Python 3.11](https://www.python.org/downloads/) (comes by default with Microsoft Store installations)
- [Node.js](https://nodejs.org/) (includes `npm`)
- Acess to a MySQL Database with the proper table architecture
  - Contact our DB admins to gain access to a test DOGUI sql DB to use. ([James Whitfield](https://github.com/whitfija) or [Brooklyn Luckett](https://github.com/BrooklynL16))

### **1. Clone the Repository**

First, clone the repository from GitHub:

```bash
git clone https://github.com/ViSiDeL/DOGUI.git

# navigate into repo
cd DOGUI

# navigate into the dogui folder, which contains the application
cd dogui
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

**WINDOWS**: If you run into an error stating that Permission is denied, run the following command:

```bash

# to fix the System.UnauthorizedAccessException,Microsoft.PowerShell.Commands.SetExecutionPolicyCommand error
Set-ExecutionPolicy -ExecutionPolicy AllSigned -Scope CurrentUser

# then activate source
venv\Scripts\activate
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

**NOTE** - If npm isn't running, and you installed NodeJS, you may need to close VSCode and reopen the terminal. Then run npm install.

Navigate back into the folder, activate your venv, and try again:

```bash
# cd into the dogui folder
cd cau-genai/dogui

# then activate source
venv\Scripts\activate

# then install
npm install 
```

**WINDOWS** - If you run into an error stating that you are not allowed to run scripts on the system, run the following command:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **5.: Store Configuration info**

DOGUI uses configuration files stored in /config to access various resources, this info is needed for various DOGUI features. Reach out to the development team to recieve premade configs that will grant access to a demo SQL table and Watson resources.

To understand how to set up the database and api connections, please see the [configuration files readme](./config/README.md). Summarized below:

**Modify the SQL connection file with your MySQL credentials:**

```bash
{
    "host": "", # MODIFY: enter the hostname that the db is hosted on
    "user": "", # MODIFY: enter your username (default = your first name, all lowercase)
    "password": "", # MODIFY: your password
    "database": "[SECRET]", # leave as is
    "port": "[SECRET]" # leave as is
}
```

Save, and rename this file to db_connection.json

**Modify the Watson info config file with your Watson credentials:**

```bash
{
    "IBM_API_KEY": "", # MODIFY: enter your IBM Cloud API key that grants access to Watson, Speech to Text, and Text to Speech
    "model_id": "ibm/granite-8b-code-instruct", # KEEP/MODIFY: uses granite 8b code instruct model by default. feel free to change to any llms available on watson
    "project_id": "", # MODIFY: enter you watson project id
    "url": "", # MODIFY: enter your IBM url (i.e. "https://us-south.ml.cloud.ibm.com")
    "texttospeech_url": "", # MODIFY: enter your full texttospeech url (i.e. "https://api.us-east.text-to-speech.watson.cloud.ibm.com/instances/full-instance-id",)
}
```

Save, and rename this file to watson_info.json

### **6. Run the Flask Application**

Start the Flask server by running:

```bash
python app.py
```

The server will start on http://127.0.0.1:4242.

### **7. Access the Application**

Open your browser and visit:

```bash
http://127.0.0.1:4242
```

## **Project Structure**

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

## **Tips**

### Running the website

 Any time you want to run the website, run app.py inside the venv that you setup. First, navigate into the dogui folder:

```bash
cd /dogui
```

then activate source

```bash
venv\Scripts\activate
```

then run the main script file

```bash
python app.py
```

### If you add new Python packages, update requirements.txt:

```bash
pip freeze > requirements.txt
```

## To add new Node modules, use:

```bash
npm install <module-name> --save
```

## If you have multiple versions of python installed, instead of the command:

```bash
python
```

use:

```bash
py -3.11
```

### If you need to run a module like pip or venv with your specific version, use the -m flag:

```bash
py -3.11 -m pip
# or
py -3.11 -m venv
```
