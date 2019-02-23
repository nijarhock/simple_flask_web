from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
app = Flask(__name__)

mysql = MySQL()

# mysql configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQLI_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor()

@app.route("/")
def main():
	return render_template('index.html')
	
@app.route("/showSignUp")
def showSignUp():
	return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
	# create user here
	
	# read request
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']
	
	# insert proses
	_hashed_passworod = generate_password_hash(_password)
	
	cursor.callproc('sp_createUser', (_name, _email, _hashed_passworod))
	
	data = cursor.fetchall()
	
	# validate data
	if len(data) is 0:
		conn.commit()
		return json.dumps({'message':'User Created Successfully !'})
	else:
		return json.dumps({'error':str(data[0])})
	
if __name__ == "__main__":
	app.run()