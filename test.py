from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello World'
@app.route('/welcome/<user_name>')
def Welcome(user_name):
    return f'Hello {user_name} welcome to flask'

@app.route('/web_page/<usr>')
def myWebPage(usr):
    return render_template("myPage.html", user=usr)

if __name__ == '__main__':
    app.run()