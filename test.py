from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/welcome')
def Welcome():
    return 'welcome to flask'

if __name__ == '__main__':
    app.run()