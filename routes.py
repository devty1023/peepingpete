from flask import Flask, render_template, request, flash
from forms import SearchForm
import info_retrieve_v4 as info_retrieve

app = Flask(__name__)
app.secret_key = 'kicsdevty1023'


@app.route('/#', methods=['GET', 'POST'])
def results():
  form = SearchForm()
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('results.html', form=form)
    else:  # form validated
      ret = info_retrieve.getCourse(form.course.data)
      if(ret == None): # bad input
        flash('No result :(')
	return render_template('results.html', form=form)
      else: # success
	table = ret
	print "LOOK HERE"
	print table
	return render_template('results.html', form=form, table=table, success=True, course=form.course.data)

  elif request.method == 'GET':
    return render_template('home.html', form=form);

@app.route('/', methods=['GET', 'POST'])
def home():
  form = SearchForm()
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('home.html', form=form)
    else:  # form validated
      ret = info_retrieve.getCourse(form.course.data)
      if(ret == None): # bad input
        flash('No result :(')
	return render_template('home.html', form=form)
      else: # success
	table = ret
	return render_template('results.html', form=form, table=table, success=True, course=form.course.data)

  elif request.method == 'GET':
    return render_template('home.html', form=form);

@app.route('/about')
def about():
  return render_template('about.html');

if __name__ == '__main__':
  app.run(debug=True);
