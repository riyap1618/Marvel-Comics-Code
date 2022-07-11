from flask import Flask, render_template, request, session, redirect, url_for
import marvel

app = Flask(__name__)
app.secret_key = b'_5#y2L"/'

# NOT FINISHED
@app.route('/')
def index():
    print(session.get('info', []))
    return render_template('index.html', info=session.get('info', []))

@app.route('/getInfo', methods=['POST'])
def getInfo():
    name = request.form.get("name")
    info = marvel.getCharacterInfo(name)
    print(info[0])
    session['info'] = info
    return redirect(url_for('index'))

@app.route('/hello')
def hello():
    return "Hello world"

