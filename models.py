from peewee import *

db = SqliteDatabase('data.db')
db.connect()

class BaseModel(Model):
	class Meta:
		database = db

class User(BaseModel):
	name = CharField(unique=True)
	password = CharField()
	salt = CharField()
	join_date = CharField()

class Post(BaseModel):
	author = ForeignKeyField(User, backref='users')
	title = CharField()
	body = CharField()
	post_time = CharField()

try:
	db.create_tables([User, Post])
except Exception as e:
	print('Error: ', e)
	db.close()