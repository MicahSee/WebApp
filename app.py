from __future__ import print_function
import sys
from flask import Flask, render_template, request, json
from werkzeug import generate_password_hash, check_password_hash
import pyrebase
app = Flask(__name__)

#beginning of firebase connection
config = {
"apiKey": "AIzaSyCDtC3dadmA_zOjmgfJPrCPYmKi9SNSBbg",
"authDomain": "nexthorizon-9094f.firebaseapp.com",
"databaseURL": "https://nexthorizon-9094f.firebaseio.com",
"projectId": "nexthorizon-9094f",
"storageBucket": "nexthorizon-9094f.appspot.com",
"messagingSenderId": "330406784555"
}

@app.route("/")
def mainpg():
    return render_template('index.html')

@app.route('/showSignUp')
def signuppg():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    name = request.form['inputName']
    email = request.form['inputEmail']
    password = request.form['inputPassword']
    #print(password+hashpass, file=sys.stderr)
    if name and email and password:
        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password("exploretheworldofdell@gmail.com","7428Micah1711")
        db = firebase.database()
        data = db.child('webusers').get(user['idToken']).val()
        if email not in data:
            hashpass = generate_password_hash(password)
            userdata = {'name':name,'email':email,'password':hashpass}
            db.child("webusers").child(email).push(userdata, user['idToken'])
            return json.dumps({'html':'<span>User created successfully</span>'})
        else:
            return json.dumps({'html':'<span>User already exists</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})











if __name__ == "__main__":
    app.run()
