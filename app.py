from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import logging
from flaskext.mysql import *


DEBUG = True
app = Flask(__name__)	#initialising flask
app.config.from_object(__name__)	#configuring flask
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

mysql = MySQL()	#initialising mysql-flask connection
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'	#db credentials being given from here
app.config['MYSQL_DATABASE_PASSWORD'] = '123456789'
app.config['MYSQL_DATABASE_DB'] = 'std_list'	#name of database to be used
app.config['MYSQL_DATABASE_HOST'] = 'localhost'	#name of lost the website is operating on
mysql.init_app(app)	#initialising connection finally

logging.basicConfig(filename='usage.log',level=logging.DEBUG)

class ReusableForm(Form):
	firstname = TextField('Firstname:', validators=[validators.DataRequired()])
	lastname = TextField('Lastname:', validators=[validators.DataRequired()])

def fetch_names(cursor, batch):
	'''
	Function that gets firstname and
	lastname of all students from a
	particular batch for alumni_batch.html
	page in the templates folder.

	## ABOUT THE ARGS ##
	cursor : To establish connection with tables
	batch : To query in database with batch
	'''
	data_temp = cursor.execute("SELECT fname, lname from temp where batch='" + batch + "\';")	#change to batch instead of branch
	data = cursor.fetchall()
	print(data)
	return data

def get_individual_data(cursor, firstname, lastname, batch):
	'''
	Function that gets experience of a
	student from a particular batch for
	individual_page.html in templates folder.

	## ABOUT THE ARGS ##
	cursor : To establish connection with tables
	firstname : To query in db with firstname
	lastname : To query in db with lastname
	batch : To query in database with batch
	'''
	#print("SELECT exp from temp where (fname='" + firstname + "', lname='" + lastname + "', batch=" + batch + ");")
	data_temp = cursor.execute("SELECT exp from temp where (fname='" + firstname + "' and lname='" + lastname + "' and batch=" + batch + ");")	#change to batch instead of branch
	data = cursor.fetchall()
	print(data)
	return data

def search_by_name(cursor, firstname, lastname):
	data_temp = cursor.execute("SELECT fname, lname, batch from temp where (fname='" + firstname + "' and lname='" + lastname + "');")	#change to batch instead of branch
	data = cursor.fetchall()
	print(data)
	return data

@app.route("/", methods=['GET', 'POST'])
def index():
	'''
	The root route, i.e. the landing page
	'''
	return render_template("index.html")	#render_template basically renders the html code of page mentioned as arg when needed

@app.route("/search", methods=['GET', 'POST'])
def search():
	'''
	The route to search for specific people
	'''
	form = ReusableForm(request.form)
	cursor = mysql.get_db().cursor()
	if(request.method == 'POST'):
		if(form.validate()):
			firstname = request.form['firstname']
			lastname = request.form['lastname']
			data = search_by_name(cursor, firstname, lastname)
			if(str(data) != "()"):
				return render_template("search.html", form=form, batch_list=data)
			else:
				return render_template("search.html", form=form, batch_list="()")
	return render_template("search.html", form=form)	#render_template basically renders the html code of page mentioned as arg when needed

@app.route("/alumni")
def alumni():
	'''
	The route, in local hosting case,
	"localhost:5000/alumni" is displayed.
	The alumni.html page is rendered here.
	'''
	return render_template("alumni.html")

@app.route("/alumni/<batch>")
def alumni_batch(batch):
	'''
	Crucial route here. /alumni/batch
	Example : /alumni/2018, /alumni/2019, etc.
	Gets the list of all students in a particular
	batch by querying in db and displays them in
	the website in alumni_batch.html page.

	batch here is a variable so it changes
	depending on when and where it is clicked from
	'''
	# Get first name and last name from batch
	# select firstname, lastname from student where batch=2020 -> SQL Statement
	# We'll get set of first and last names in the format
	#((firstname1, lastname1),(firstname2, lastname2),(firstname3,lastname3),..)
	cursor = mysql.get_db().cursor()	#creating cursor that's needed for querying from program
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
	'''
	This is an individual_page for everyone.
	Contets change depending on the name of
	student that one clicks on.
	Example of route : /alumni/2020/XYZ-ABC, /alumni/2019/XYZ-ABC
	In both cases, XYZ, ABC are firstname and lastname respectively
	and the batch is 2020 and 2019 respectively.

	batch, firstname and lastname are vars here
	and change depending on where they are clicked
	from and when they are clicked.
	'''
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
	'''
	Error message displayed if Page
	not found or user tries accessing
	a page that doesn't exist or have access to
	'''
	return render_template("404.html")


@app.errorhandler(500)
def application_error(e):
	'''
	Error handler for unexpected errors.
	'''
	return 'Sorry, unexpected error: {}'.format(e), 500


if(__name__ == "__main__"):
	app.run(host="localhost", port=5000)
