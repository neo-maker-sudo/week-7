from flask import Flask, session, redirect, request, render_template, url_for, jsonify, abort
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
import os
import json
app = Flask(__name__)
db = SQLAlchemy(app)

# session
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMENENT_SESSION_LIFETIME'] = timedelta(days=1)

# database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
#mysql+pymysql://neo:neoneo@localhost:3306/website
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## model for flask_sqlalchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    query = User.query.filter_by(username=username).first()
    if query:
        return redirect(url_for('error', message=username,name=name))
    else:
        new_user = User(name,username,password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password= request.form['password']
    query = User.query.filter_by(username=username).first()
    if query and query.password == password :
        session['username'] = query.username
        session.permenent = True
        return redirect(url_for('member'))
    else:
        return redirect(url_for('error', message=username))
    
@app.route('/signout', methods=['GET'])
def signout():
    session['username'] = False
    return redirect(url_for('index'))

@app.route('/member/')
def member():
    sesson_username = session.get('username')
    query = User.query.filter_by(username=sesson_username).first()
    if sesson_username:
        return render_template("member.html", name=query.name)
    else:
        return redirect(url_for('index'))


@app.route('/error/')
def error():
    message = request.args.get("message", None)
    name = request.args.get("name",None)
    return render_template("error.html", message=message,name=name)

@app.route('/api/users')
def search():
    sesson_username = session.get('username')
    username = request.args.get('username',None)
    query = User.query.filter_by(username=username).first()
    if query and sesson_username:
        return jsonify({"data": {'id': query.id, 'name': query.name, 'username': query.username}})
    else:
        return jsonify({'data':'null'})


@app.route('/api/user', methods=['POST'])
def update():
    sesson_username = session.get('username')
    newname = request.json['name']
    query = User.query.filter_by(username=sesson_username).first()
    if newname == '':
        return jsonify({'error': 'empty value'})
    elif query is None:
        return jsonify({'error':'database error'})
    elif query.name == newname:
        return jsonify({'error':'same name error'})
    elif query and sesson_username:
        queryAll = User.query.filter_by(name=newname).first()
        if queryAll:
            return jsonify({'error':'this name already taken'})
        else:
            query.name = newname
            db.session.commit()
            return jsonify({'ok': True})
    else:
        return jsonify({'error': True})



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=3000)



