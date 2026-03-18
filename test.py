from flask import Flask, render_template, jsonify, make_response, request
from pydantic import BaseModel, Field, ValidationError
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.before_request
def log_request_info():
    app.logger.info(f"..client Request: {request.method} {request.url}")

@app.after_request
def log_response_info(response):
    app.logger.info(f"...Response from server: {response.status}")
    return response

class SoftwareEngg(BaseModel):
    Name: str
    Role: str
@app.route('/json_resp', methods = ['GET', 'POST'])
def myjsonPage():
    try:
        data = SoftwareEngg(**request.get_json())
        app.logger.info(f"...parsed input:{data}")
        testDict = [{"Name":"Linus Torvalds", "Role":"Software architect"}]
        if request.method == 'POST':
            new_data = request.get_json()
            testDict.append(new_data)
            return make_response(jsonify(testDict), 200)
    except ValidationError as e:
        app.logger.error(f"...validation failed:{e}")
        return make_response(jsonify(e.errors()), 400)    
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