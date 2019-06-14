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
			password=sha256(psw.encode()), 
			join_date=datetime.now())

@app.route('/login', methods=['POST'])
def login():
	name = request.form['name']
	psw = request.form['password']
	try:
		query = User.get(User.name == name)
	except Exception as e:
		query = False
		print('Error: ', e)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)