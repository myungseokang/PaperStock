from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/hello/<string:to>")
def helloTo(to="NoBody"):
    return render_template("index.html", to=to)

@app.route("/world", methods=["GET", "POST"])
def world():
    return "world %s" % (request.method,)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
