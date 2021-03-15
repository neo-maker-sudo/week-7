from flask import Flask, session, redirect, request, render_template
from datetime import timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMENENT_SESSION_LIFETIME'] = timedelta(days=1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password= request.form['password']
    if username == 'test' and password == 'test':
        session['username'] = username
        session.permenent = True
        return redirect("/member/")
    else:
        return redirect("/error/")
    
@app.route('/signout', methods=['GET'])
def signout():
    session['username'] = False
    return redirect("/"), 302

@app.route('/member/')
def member():
    username = session.get('username')
    if username:
        return render_template("member.html")
    else:
        return redirect("/")

@app.route('/error/')
def error():
    return render_template("error.html")

if __name__ == '__main__':
    app.run(debug=True, port=3000)
