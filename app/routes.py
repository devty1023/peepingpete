from flask import Flask, render_template, request, flash
from forms import SearchForm
import info_retrieve

app = Flask(__name__)
app.secret_key = 'kicsdevty1023'

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
        flash('Bad Course Name! (or other bad issues)')
	return render_template('home.html', form=form)
      else:
	flash(ret)
	return render_template('home.html', form=form)

  elif request.method == 'GET':
    return render_template('home.html', form=form);

@app.route('/about')
def about():
  return render_template('about.html');

if __name__ == '__main__':
  app.run(debug=True);
