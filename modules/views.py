from __init__ import app

@app.route("/")
@app.route("index")
def greet():
    return "Hello World"