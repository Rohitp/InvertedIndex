from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
from processText import process, processSearch
import sys 

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@app.route("/index")
def greet(id=None, name = "Rohit"):
    return render_template("welcome.html")

@app.route("/search")
def search():
    searchResult = processSearch(request.args.get("q"))
    return render_template("results.html", searchResult=searchResult)

@app.route("/insert",  methods = ['POST'])
@cross_origin()
def insert():
    data = request.form.to_dict();
    pos = process(data)
    return jsonify({"code": 1, "message": "INSERTED"})

app.run(debug=True)