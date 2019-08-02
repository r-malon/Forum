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

class Category(BaseModel):
	name = CharField(unique=True)
	icon_name = CharField()

class Post(BaseModel):
	author = ForeignKeyField(User, backref='posts')
	category = ForeignKeyField(Category, backref='posts')
	title = CharField()
	body = CharField()
	post_time = CharField()

class Comment(BaseModel):
	author = ForeignKeyField(User, backref='comments')
	post = ForeignKeyField(Post, backref='comments')
	body = CharField()
	post_time = CharField()

try:
	db.create_tables([User, Post, Category])
except Exception as e:
	print('Error: ', e)
	db.close()