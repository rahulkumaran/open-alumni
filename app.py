from flask import Flask, render_template, flash, request, redirect, url_for
import logging


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
logging.basicConfig(filename='usage.log',level=logging.DEBUG)

@app.route("/", methods=['GET', 'POST'])
def index():
	return render_template("index.html")

@app.route("/alumni")
def alumni():
	return render_template("alumni.html")

@app.route("/alumni/<batch>")
def alumni_batch(batch):
	if(batch=="2020"):
		return render_template("alumni_batch.html")
	elif(batch=="2021"):
		return render_template("alumni_batch.html")
	elif(batch=="2022"):
		return render_template("alumni_batch.html")
	elif(batch=="2023"):
		return render_template("alumni_batch.html")
	else:
		return render_template("404.html")

@app.route("/alumni/<string:batch>/<string:firstname>-<string:lastname>")
def individual_page(batch, firstname, lastname):
	if(batch=="2020"):
		return render_template("individual_page.html", batch=batch, firstname=firstname, lastname=lastname)
	elif(batch=="2021"):
		return render_template("individual_page.html", batch=batch, firstname=firstname, lastname=lastname)
	elif(batch=="2022"):
		return render_template("individual_page.html", batch=batch, firstname=firstname, lastname=lastname)
	elif(batch=="2023"):
		return render_template("individual_page.html", batch=batch, firstname=firstname, lastname=lastname)
	else:
		return render_template("404.html")



@app.errorhandler(404) 
def not_found(e):
	return render_template("404.html")


@app.errorhandler(500)
def application_error(e):
	return 'Sorry, unexpected error: {}'.format(e), 500


if(__name__ == "__main__"):
	app.run(host="localhost", port="8080")
