from flask import Flask, render_template, flash, request, redirect, url_for, session
from flaskext.mysql import *
from flask_login import current_user
from forms import *
import logging
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


DEBUG = True
app = Flask(__name__)	#initialising flask
app.config.from_object(__name__)	#configuring flask
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'	#db credentials being given from here
app.config['MYSQL_DATABASE_PASSWORD'] = '123456789'
app.config['MYSQL_DATABASE_DB'] = 'std_list'	#name of database to be used
app.config['MYSQL_DATABASE_HOST'] = 'localhost'	#name of lost the website is operating on
mysql.init_app(app)	#initialising connection finally

conn = mysql.connect()

conn.autocommit = True

logging.basicConfig(filename='usage.log',level=logging.DEBUG)

is_user_active = False


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
	data_temp = cursor.execute("SELECT Fname, Lname from Details where Batch='" + batch + "\';")	#change to batch instead of branch
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

	Returns experience of the students whose
	firstname, lastname and batch match.
	'''
	#print("SELECT exp from temp where (fname='" + firstname + "', lname='" + lastname + "', batch=" + batch + ");")
	rollno = get_rollno(cursor, firstname, lastname, batch)
	data_temp = cursor.execute("SELECT experiance from Exp where Rollno=" + rollno + ";")	#change to batch instead of branch
	data = cursor.fetchall()
	print(data)
	return data

def search_by_name(cursor, firstname, lastname):
	'''
	Gets the firstname, lastname and batch
	from the table temp given a firstname and
	lastname in the /search route.

	Returns all fields that match the given
	first and lastname by the user.
	'''
	data_temp = cursor.execute("SELECT Fname, Lname, Batch from Details where (fname='" + firstname + "' and lname='" + lastname + "');")	#change to batch instead of branch
	data = cursor.fetchall()
	print(data)
	return data

def update_exp(cursor, experience, firstname, lastname, batch):
	rollno = get_rollno(cursor, firstname, lastname, batch)
	data_temp = cursor.execute("UPDATE Exp SET experiance='" + experience + "' where Rollno=" + rollno + ";")
	conn.autocommit = True
	data = cursor.fetchall()
	print(data)

def update_contact(cursor, email, firstname, lastname, batch):
	rollno = get_rollno(cursor, firstname, lastname, batch)
	data_temp = cursor.execute("UPDATE Contact_Details SET EmailID='" + email + "' where Rollno=" + rollno + ";")
	conn.autocommit = True
	data = cursor.fetchall()
	print(data)

def update_location(cursor, location, firstname, lastname, batch):
	rollno = get_rollno(cursor, firstname, lastname, batch)
	data_temp = cursor.execute("UPDATE Current_Location SET Location='" + location + "' where Rollno=" + rollno + ";")
	conn.autocommit = True
	data = cursor.fetchall()
	print(data)

def get_loc(cursor,firstname, lastname, batch):
	rollno = get_rollno(cursor, firstname, lastname, batch)
	data_temp = cursor.execute("SELECT Location from Current_Location where Rollno=" + rollno + ";")
	data = cursor.fetchall()
	print(data)
	return data

def get_email(cursor, firstname, lastname, batch):
	rollno = get_rollno(cursor, firstname, lastname, batch)
	data_temp = cursor.execute("SELECT EmailID from Contact_Details where Rollno=" + rollno + ";")
	data = cursor.fetchall()
	print(data[0][0])
	return data[0][0]


def get_rollno(cursor, firstname, lastname, batch):
	print("in here")
	data_temp = cursor.execute("SELECT Rollno from Details where (Fname='" + firstname + "' and Lname='" + lastname + "' and Batch=" + batch + ");")
	data = cursor.fetchall()
	print(data[0][0])
	return data[0][0]

@app.route("/", methods=['GET', 'POST'])
def index():
	'''
	The root route, i.e. the landing page
	'''
	return render_template("index.html")	#render_template basically renders the html code of page mentioned as arg when needed

@app.route("/search", methods=['GET', 'POST'])
def search():
	'''
	The route to search for specific people.
	One can give a particular firstname and
	lastname and we return all people whose
	first and lastnames match with the name
	entered by the user in the /search form.
	'''
	form = ReusableForm(request.form)	#Creating a form object
	cursor = mysql.get_db().cursor()
	if(request.method == 'POST'):		#If the user submits data in the Form
		if(form.validate()):		#If form is validated
			firstname = request.form['firstname']	#Get firstname
			lastname = request.form['lastname']		#Get lastname
			data = search_by_name(cursor, firstname, lastname)	#Search DB for given first and lastname
			if(str(data) != "()"):	#Check if null tuple
				return render_template("search.html", form=form, batch_list=data)	#Pass data if not null tuple
			else:	#if null tuple, pass the string format of null tuple --> "()"
				return render_template("search.html", form=form, batch_list="()")
	return render_template("search.html", form=form)

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
		loc = get_loc(cursor, firstname, lastname, batch)
		email = get_email(cursor, firstname, lastname, batch)
		print(data)
		return render_template("individual_page.html", batch=batch, firstname=firstname, lastname=lastname, exp=data[0][0], location=loc[0][0], email=email)
	elif(batch=="2019"):
		data = get_individual_data(cursor, firstname, lastname, batch)
		loc = get_loc(cursor, firstname, lastname, batch)
		email = get_email(cursor, firstname, lastname, batch)
		return render_template("individual_page.html", batch=batch, firstname=firstname, lastname=lastname, exp=data[0][0], location=loc[0][0], email=email)
	elif(batch=="2020"):
		data = get_individual_data(cursor, firstname, lastname, batch)
		loc = get_loc(cursor, firstname, lastname, batch)
		email = get_email(cursor, firstname, lastname, batch)
		return render_template("individual_page.html", batch=batch, firstname=firstname, lastname=lastname, exp=data[0][0], location=loc[0][0], email=email)
	elif(batch=="2021"):
		data = get_individual_data(cursor, firstname, lastname, batch)
		loc = get_loc(cursor, firstname, lastname, batch)
		email = get_email(cursor, firstname, lastname, batch)
		return render_template("individual_page.html", batch=batch, firstname=firstname, lastname=lastname, exp=data[0][0], location=loc[0][0], email=email)
	else:
		return render_template("404.html")

@app.route("/update-experience", methods=['GET','POST'])
def update_experience():
	form = UpdateForm(request.form)	#Creating a form object
	conn.autocommit = True
	cursor = mysql.get_db().cursor()
	if(request.method == 'POST'):		#If the user submits data in the Form
		if(form.validate()):		#If form is validated
			firstname = request.form['firstname']	#Get firstname
			lastname = request.form['lastname']	#Get firstname
			batch = request.form['batch']	#Get firstname
			experience = request.form['update']	#Get firstname
			update_exp(cursor, experience, firstname, lastname, batch)
			#flash("Done updating your experience.")
			print(firstname, lastname, experience, batch)
			return render_template("index.html")
	return render_template("update_experience.html", form=form)


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
	app.run(host="localhost", port=8000)
