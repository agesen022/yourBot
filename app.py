from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index(title="your bot"):
    return render_template('index.html',title=title)

@app.route('/good')
def good():
    name = "Good"
    return name

## おまじない
if __name__ == "__main__":
    app.run(debug=True)