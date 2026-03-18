from flask import Flask, render_template, jsonify, make_response

app = Flask(__name__)

@app.route('/json_resp', methods = ['GET', 'POST'])
def myjsonPage():
    testDict = {"Name":"Linus Torvalds", "Role":"Software architect"}
    return make_response(jsonify(testDict), 200)



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