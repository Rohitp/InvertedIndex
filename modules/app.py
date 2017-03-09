from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
from processText import process
import sys 

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@app.route("/index")
@app.route("/index/<int:id>/<string:name>")
def greet(id=None, name = "Rohit"):
    return "Hello World "+str(id)+name

@app.route("/search")
def search():
    return render_template("results.html", query=request.args.get("q"))

@app.route("/insert",  methods = ['POST'])
@cross_origin()
def insert():
    data = request.form.to_dict();
    pos = process(data)
    return jsonify(pos)

app.run(debug=True)