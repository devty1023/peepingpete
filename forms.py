from flask.ext.wtf import Form, TextField, SubmitField, validators, ValidationError
 
class SearchForm(Form):
  course = TextField("Course", [validators.Required()])
  submit = SubmitField("Submit")
