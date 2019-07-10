from flask import *
from models import *
from datetime import datetime
from hashlib import sha256
from random import choice
from uuid import uuid4

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'hey_baby'
#session['logged'] = False #needs active request

error_msg = [
	'Prepare for unforeseen consequences', 
	'And another page bites the dust...', 
	'Away with you, vile error!', 
	'Mayday, Mayday!!!', 
	'O problema é na mangueira!', 
	'Flask, we have a problem!']

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/signup', methods=['POST'])
def signup():
	name = request.form['name']
	psw = request.form['password']
	salt = uuid4().hex
	try:
		User.create(
			name=name, 
			password=sha256((psw + salt).encode()).hexdigest(), 
			salt=salt, 
			join_date=str(datetime.utcnow())[:19])
		session['username'] = name
		session['logged'] = True
		return redirect(f'/user/{name}')
	except Exception as e:
		flash('Signup failed!')
		return redirect('/home')

@app.route('/login', methods=['POST'])
def login():
	name = request.form['name']
	psw = request.form['password']
	try:
		query = User.get(User.name == name)
		if query.password == sha256((psw + query.salt).encode()).hexdigest():
			session['username'] = name
			session['logged'] = True
			return redirect(f'/user/{name}')
		raise Exception
	except Exception as e:
		flash('Login failed!')
		return redirect('/home')

@app.route('/user/<username>')
def user_page(username):
	try:
		query = User.get(User.name == username)
		return render_template('userpage.html', 
			username=query.name, 
			join_date=query.join_date, 
			img_src=f"https://gravatar.com/avatar/{sha256(username.encode()).hexdigest()}?d=identicon&s=128")
	except Exception as e:
		flash('User not found')
		return redirect('/home')

@app.route('/create_post', methods=['POST'])
def create_post():
	title = request.form['title']
	body = request.form['body']
	try:
		if not session['logged']:
			flash('Login required!')
			raise Exception
		post = Post.create(
			author=User.get(User.name == session['username']), #use id?
			title=title, 
			body=body, 
			post_time=str(datetime.utcnow())[:19])
		return redirect(f'/post/{post.id}')
	except Exception as e:
		flash('Posting failed!')
		return redirect('/home')

@app.route('/post/<post_id>')
def post(post_id):
	try:
		query = Post.get(Post.id == post_id)
		return render_template('post.html', 
			author=User.get(User.id == query.author_id).name, 
			title=query.title, 
			body=query.body, 
			time=query.post_time)
	except Exception as e:
		flash('Post not found')
		return redirect('/home')

@app.route('/logout')
def logout():
	session['logged'] = False
	try:
		session.pop('username')
	except KeyError:
		return redirect('/home')
	return render_template('logout.html')

@app.errorhandler(404)
def not_found(e):
	return render_template('404.html', msg=choice(error_msg)), 404

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)