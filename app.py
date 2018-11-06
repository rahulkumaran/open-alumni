from flask import Flask, render_template, flash, request, redirect, url_for
import logging
from flaskext.mysql import *


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456789'
app.config['MYSQL_DATABASE_DB'] = 'std_list'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

logging.basicConfig(filename='usage.log',level=logging.DEBUG)

def fetch_names(cursor, batch):
	data_temp = cursor.execute("SELECT fname, lname from temp where batch='" + batch + "\';")	#change to batch instead of branch
	data = cursor.fetchall()
	print(data)
	return data

def get_individual_data(cursor, firstname, lastname, batch):
	#print("SELECT exp from temp where (fname='" + firstname + "', lname='" + lastname + "', batch=" + batch + ");")
	data_temp = cursor.execute("SELECT exp from temp where (fname='" + firstname + "' and lname='" + lastname + "' and batch=" + batch + ");")	#change to batch instead of branch
	data = cursor.fetchall()
	print(data)
	return data

@app.route("/", methods=['GET', 'POST'])
def index():
	return render_template("index.html")

@app.route("/alumni")
def alumni():
	return render_template("alumni.html")

@app.route("/alumni/<batch>")
def alumni_batch(batch):

	# Get first name and last name from batch
	# select firstname, lastname from student where batch=2020 -> SQL Statement
	# We'll get set of first and last names
	# Manipulate to get [[firstname1, lastname1],[firstname2, lastname2],[firstname3,lastname3],..]
	cursor = mysql.get_db().cursor()
	#print(cursor)
	print(batch)
	if(batch=="2018"):
		data = fetch_names(cursor, "2018")
		return render_template("alumni_batch.html", batch=batch, batch_list=data)
	elif(batch=="2019"):
		data = fetch_names(cursor, "2019")
		return render_template("alumni_batch.html", batch=batch, batch_list=data)
	elif(batch=="2020"):
		data = fetch_names(cursor, "2020")
		return render_template("alumni_batch.html", batch=batch, batch_list=data)
	elif(batch=="2021"):
		data = fetch_names(cursor, "2021")
		return render_template("alumni_batch.html", batch=batch, batch_list=data)
	else:
		return render_template("404.html")

@app.route("/alumni/<string:batch>/<string:firstname>-<string:lastname>")
def individual_page(batch, firstname, lastname):
	cursor = mysql.get_db().cursor()
	if(batch=="2018"):
		data = get_individual_data(cursor, firstname, lastname, batch)
		print(data)
		return render_template("individual_page.html", batch=batch, firstname=firstname, lastname=lastname, exp=data[0][0])
	elif(batch=="2019"):
		data = get_individual_data(cursor, firstname, lastname, batch)
		return render_template("individual_page.html", batch=batch, firstname=firstname, lastname=lastname, exp=data[0][0])
	elif(batch=="2020"):
		data = get_individual_data(cursor, firstname, lastname, batch)
		return render_template("individual_page.html", batch=batch, firstname=firstname, lastname=lastname, exp=data[0][0])
	elif(batch=="2021"):
		data = get_individual_data(cursor, firstname, lastname, batch)
		return render_template("individual_page.html", batch=batch, firstname=firstname, lastname=lastname, exp=data[0][0])
	else:
		return render_template("404.html")



@app.errorhandler(404)
def not_found(e):
	return render_template("404.html")


@app.errorhandler(500)
def application_error(e):
	return 'Sorry, unexpected error: {}'.format(e), 500


if(__name__ == "__main__"):
	app.run(host="localhost", port=5000)
