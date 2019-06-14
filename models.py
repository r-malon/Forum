from peewee import *

db = SqliteDatabase('users.db')
db.connect()

class BaseModel(Model):
	class Meta:
		database = db

class User(BaseModel):
	name = CharField(unique=True)
	password = CharField()
	join_date = CharField()

try:
	db.create_tables([User])
except Exception as e:
	print('Error: ', e)