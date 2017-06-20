from __future__ import print_function
import sys
from flask import Flask, render_template, request, json
from werkzeug import generate_password_hash, check_password_hash
import pyrebase
app = Flask(__name__)

#beginning of firebase connection
config = {}

@app.route("/")
def mainpg():
    return render_template('index.html')

@app.route('/showSignUp')
def signuppg():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    name = request.form['inputName']
    username = request.form['inputUsername']
    password = request.form['inputPassword']
    #print(password+hashpass, file=sys.stderr)
    if name and username and password:
        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password("exploretheworldofdell@gmail.com","7428Micah1711")
        db = firebase.database()
        data = db.child('webusers').get(user['idToken']).val()
        if username not in data:
            hashpass = generate_password_hash(password)
            userdata = {'name':name,'username':username,'password':hashpass}
            db.child("webusers").child(username).set(userdata, user['idToken'])
            return json.dumps({'html':'<span>User created successfully</span>'})
        else:
            return json.dumps({'html':'<span>User already exists</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})











if __name__ == "__main__":
    app.run(debug=True, port=80)
