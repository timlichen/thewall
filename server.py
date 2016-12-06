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
	query = "INSERT INTO friends (firstname, lastname, email, password, created_at, updated_at) VALUES (:firstname, :lastname, :email, :password, NOW(), NOW())"
	data = {
			'firstname': request.form['firstname'],
			'lastname': request.form['lastname'],
			'email': request.form['email'],
			'password': request.form['password']
			}
	mysql.query_db,(query, data)
	info = {
			"firstname": request.form['firstname'],
			"lastname": request.form['lastname'],
			"email": request.form['email'],
			"password": request.form['password']
			}
	if len(request.form['firstname']) < 2:
		flash('please fill in first name!')
	elif len(request.form['lastname']) < 1:
		flash('please fill in last name!')
	elif len(request.form['email']) < 2:
		flash('please fill in email!')
	elif not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid email!")
	elif len(request.form['password']) < 8:
		flash('please fill in password!')
	elif len(request.form['confirmed_password']) < 8:
		flash('please confirm your password!')
		flash('the passwords do not match!')
	else:
		flash('Congrats! You have signed up!')


	return render_template('registration.html', info = info)

@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/wall')
def wall():
	# info = {
	# 		"firstname": request.form['firstname'],
	# 		"lastname": request.form['lastname'],
	# 		"email": request.form['email'],
	# 		"password": request.form['password']
	# 		}
	# print info
	return render_template('wall.html')

app.run(debug=True)