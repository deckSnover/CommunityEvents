from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://community_admin:password@localhost/communityevents'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    date = Column(DateTime)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sender = Column(String)
    receiver = Column(String)
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine('postgresql://community_admin:password@localhost/communityevents')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    events = session.query(Event).all()
    messages = session.query(Message).all()
    return render_template('index.html', events=events, messages=messages)

@app.route('/add', methods=['POST'])
def add_event():
    name = request.form['name']
    description = request.form['description']
    date = request.form['date']
    new_event = Event(name=name, description=description, date=datetime.datetime.strptime(date, '%Y-%m-%d'))
    session.add(new_event)
    session.commit()
    return redirect(url_for('index'))

@app.route('/send_message', methods=['POST'])
def send_message():
    sender = request.form['sender']
    receiver = request.form['receiver']
    content = request.form['content']
    new_message = Message(sender=sender, receiver=receiver, content=content)
    session.add(new_message)
    session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
