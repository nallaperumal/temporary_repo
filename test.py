from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/welcome/<username>')
def Welcome(user_name):
    return f'Hello {username} welcome to flask'

if __name__ == '__main__':
    app.run()