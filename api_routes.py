#!flask/bin/python
from flask import Flask, jsonify, request
import info_retrieve_v6

app = Flask(__name__)


@app.route('/api/v1.0/course/<string:course>', methods = ['GET', 'POST'])
def get_cousre(course):
    if request.method == 'POST':
        return "POST request is not supported u smarty pants"
    elif request.method == 'GET':
        ret = info_retrieve_v6.getCourse(course)
        if ret == None:
           return jsonify( { "error": "COURSE NOT FOUND"} )
        return jsonify(ret)



@app.route('/api/v1.0/crn/<string:crn>', methods = ['GET', 'POST'])
def get_crn(course):
    if request.method == 'POST':
        return "POST request is not supported u smarty pants"
    elif request.method == 'GET':
        ret = info_retrieve_v6.getCourse(crn)
        if ret == None:
           return jsonify( { "error": "COURSE NOT FOUND"} )
        return jsonify(ret)
		
@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
   app.run(debug = True)


