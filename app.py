from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from datetime import datetime
from db import db
import psycopg2
import urllib.parse as urlparse
import os

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    spotify_id = db.Column(db.Text, unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_updated = db.Column(db.TIMESTAMP, nullable=False)
    city = db.Column(db.Text, nullable=False)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    engine = create_engine(os.environ['DB_URI'])
    connection = engine.connect()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        select_query = '''SELECT * FROM "Users" WHERE email='%s' AND password='%s';''' % ( email, password )
        User_data = connection.execute( select_query ).fetchone()

        if not User_data and email != None:
            error = 'Wrong email or password' 
        else:
            spotify_id = User_data[3]
            date_created = User_data[4]
            date_updated = User_data[5]
            city = User_data[6]

            user = User(email=email, 
                        password=password,
                        spotify_id=spotify_id,
                        date_created=date_created,
                        date_updated=date_updated,
                        city=city)

            return 'Welcome Back %s' % (user.email)

    return render_template('login.html', error=error)

@app.route('/Users')
def contacts():
        select_query = 'SELECT * FROM public."Users"'
        cur.execute(select_query )
        rows = cur.fetchall()

        my_list = []
        for row in rows:
            my_list.append(row[1])

        return render_template('template.html',  results=my_list)

if __name__ == '__main__':
    app.run(threaded=true)
