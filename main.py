from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('signup.html')
    return template.render()

@app.route("/", methods=['POST'])
def validate_form():
    #variables
    _error = ""
    usererror = ""
    passerror = ""
    emailerror = "That's not a valid emial"
    email_valid = True
    #emailmess = ""
    #form variables
    username = request.form['username']
    password = request.form['password']
    verifypasswd = request.form['verifypasswd']
    email = request.form['email']
    #username validation
    _error = validate_(username)
    
    if _error != "":
        usererror = "Username "+_error
        username = ""
    #password validation
    if password == verifypasswd:
        _error = validate_(password)
    else:
        passerror = "Passwords do not match"
    
    if _error != "":
        passerror = "Password "+_error

    #email validation
    if email != "":
        email_valid = validate_email(email)
    
    if not usererror and not passerror and email_valid:
        return redirect('/signup_welcome?username={0}'.format(username))
    elif email_valid:
        template = jinja_env.get_template('signup.html')
        return template.render(usererror=usererror,
            passerror=passerror,
            username=username,
            email=email)
    else:
        template = jinja_env.get_template('signup.html')
        return template.render(usererror=usererror,
            passerror=passerror,
            username=username,
            emailerror=emailerror,
            email=email)


@app.route('/signup_welcome')
def welcome():
    usererror = request.args.get('username')
    template =  jinja_env.get_template('welcome.html')
    return template.render(username = username)
    
def validate_email(email):
    if len(email)<3 or len(email)>20:
        return False
    else:
        symAT =0
        dot =0

        for char in email:
            if char == " ":
                return False
            elif char == "@":
                symAT +=1
            elif char == ".":
                dot += 1
        if symAT!=1 or dot!=1:
            return False
    return True


def validate_(inputdata):
    if inputdata == '':
        return " is blank"
    elif len(inputdata)<3:
        return " must be at least 3 characters"
    elif len(inputdata)>20:
        return " exceeds 20 character max"
    else:
        for letter in inputdata:
             if letter == " ":
                 return " cannot contain spaces"
    return ""

    
    

app.run()