from flask import Flask

app = Flask(__name__)

f = open("template.html")
template = f.read()
f.close()

@app.route("/")
def root():
    return template + "<h1>Placeholder</h1>" + "</body></html>"

app.run('0.0.0.0', 7444)