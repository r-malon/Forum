from flask import *
from models import *
from datetime import datetime
from hashlib import sha256

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'hey_baby'

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/signup', methods=['POST'])
def signup():
	name = request.form['name']
	psw = request.form['password']
	try:
		query = User.get(User.name == name)
	except Exception as e:
		query = False
		print('Error: ', e)
	if name is not query:
		User.create(
			name=name, 
			password=sha256(psw.encode()).hexdigest(), 
			join_date=str(datetime.utcnow()))
		session['username'] = name
		session['logged'] = True
		return redirect(f'/user/<{name}>')

@app.route('/login', methods=['POST'])
def login():
	name = request.form['name']
	psw = request.form['password']
	try:
		query = User.get(User.name == name)
		if query.password == sha256(psw.encode()).hexdigest():
			session['username'] = name
			session['logged'] = True
		return redirect(f'/user/<{name}>')
	except Exception as e:
		print('Error: ', e)
		return redirect('/home')

@app.route('/user/<username>')
def user_page(username):
	try:
		query = User.get(User.name == username)
		return render_template('userpage.html', 
			username=query.name, 
			img_src=f"https://gravatar.com/avatar/{sha256(username.encode()).hexdigest()}?d=identicon&s=128")
	except Exception as e:
		print('Error: ', e)
		return redirect('/home')

@app.route('/logout')
def logout():
	try:
		session.pop('username')
	except KeyError:
		session['logged'] = False
		return redirect('/home')
	session['logged'] = False
	return render_template('logout.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)