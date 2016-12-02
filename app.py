from flask import Flask, redirect, request, render_template, url_for

app = Flask(__name__)
app.secret_key = "canx"

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
