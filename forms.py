class ReusableForm(Form):
	'''
	Form to perform the search functionality
	in the /search route where one needs to
	type in the first and last name
	'''
	firstname = TextField('Firstname:', validators=[validators.DataRequired()])
	lastname = TextField('Lastname:', validators=[validators.DataRequired()])

class LoginForm(Form):
	email = TextField('Email', validators=[validators.DataRequired()])
	password = TextField('Password', validators=[validators.DataRequired()])
