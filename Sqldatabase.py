from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine('postgresql://user:password@localhost/communityevents')
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

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Example of inserting a message
message = Message(sender='igordrims', receiver='CynthiaCristina', content='Hello Cynthia!')
session.add(message)
session.commit()

# Example of querying messages between two users
messages = session.query(Message).filter(
    ((Message.sender == 'igordrims') & (Message.receiver == 'CynthiaCristina')) |
    ((Message.sender == 'CynthiaCristina') & (Message.receiver == 'igordrims'))
).all()

for message in messages:
    print(message.sender, message.receiver, message.content, message.timestamp)
