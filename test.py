from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/json_resp')
def myjsonPage():
    testDict = {"Name":"Linus Torvalds", "Role":"Software architect"}
    return jsonify(testDict)



@app.route('/')
def hello_world():
    return 'Hello World'
@app.route('/welcome/<user_name>')
def Welcome(user_name):
    return f'Hello {user_name} welcome to flask'

@app.route('/web_page/<usr>')
def myWebPage(usr):
    # usr = "user123"
    return render_template("myPage.html", user=usr)

if __name__ == '__main__':
    app.run()