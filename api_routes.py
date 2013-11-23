#!flask/bin/python
from flask import Flask, jsonify
import info_retrieve_v4

app = Flask(__name__)


@app.route('/api/v1.0/<string:course>', methods = ['GET'])
def get_tasks(course):
    return jsonify( info_retrieve_v4.getCourse(course) )
		
@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
   app.run(debug = True)


