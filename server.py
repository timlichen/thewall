from flask import Flask, render_template, request, redirect, session, flash
import re
from mysqlconnection import MySQLConnector
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "paeglregklr"
mysql = MySQLConnector(app, 'wall')


@app.route('/')
def registration():
	return render_template('registration.html')

@app.route('/result', methods=['post'])
def result():
	flag = False

	if len(request.form['firstname']) < 2:
		flag = True
		flash('please fill in first name!')
	elif len(request.form['lastname']) < 1:
		flag = True
		flash('please fill in last name!')
	elif len(request.form['email']) < 2:
		flag = True
		flash('please fill in email!')
	elif not EMAIL_REGEX.match(request.form['email']):
		flag = True
		flash("Invalid email!")
	elif len(request.form['password']) < 8:
		flag = True
		flash('please fill in password!')
	elif len(request.form['confirmed_password']) < 8:
		flag = True
		flash('please confirm your password!')
		flash('the passwords do not match!')

	if flag:
		return redirect("/")
	else:
		query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:firstname, :lastname, :email, :password, NOW(), NOW())"
		info = {
				'firstname': request.form['firstname'],
				'lastname': request.form['lastname'],
				'email': request.form['email'],
				'password': request.form['password']
				}
		user_id = mysql.query_db(query, info)
		session['user_id'] = user_id
		return redirect("/wall")

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/loginProcess', methods=["POST"])
def loginProc():
	query = "SELECT id, first_name, last_name, password from users WHERE first_name = :first AND last_name = :last AND password = :pass"
	data = {
		"first": request.form['firstname'],
		"last": request.form['lastname'],
		"pass": request.form['password']
	}
	user =  mysql.query_db(query, data)

	if user:
		session['user_id'] = user[0]['id']
		return redirect('/wall')
	else:
		return redirect('/login')

@app.route('/logoff')
def logoff():
	session.clear()
	return render_template('login.html')

@app.route('/wall')
def wall():
	print session['user_id']
	return render_template('wall.html')

app.run(debug=True)
