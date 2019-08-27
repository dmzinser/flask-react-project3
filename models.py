from peewee import *
from flask_login import UserMixin
import datetime
import os
from playhouse.db_url import connect

# DATABASE = connect(os.environ.get('DATABASE_URL'))
DATABASE = SqliteDatabase('photos.sqlite')

class User(UserMixin, Model):
  username = CharField(unique=True)
  email = CharField(unique=True)
  password = CharField()
  image = CharField()

  class Meta:
    database = DATABASE

class Photo(Model):
  title = CharField()
  description = CharField()
  longitude = CharField()
  latitude = CharField()
  file_location = CharField()
  user = ForeignKeyField(User, backref='photos')
  
  class Meta:
    database = DATABASE

def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User, Photo], safe=True)
  print("Tables Created")
  DATABASE.close()