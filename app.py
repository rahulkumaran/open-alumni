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

if(__name__ == "__main__"):
	app.run(host="localhost", port="8080")
