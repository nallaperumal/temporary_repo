from flask import Flask, render_template, jsonify, make_response, request
from pydantic import BaseModel, Field, ValidationError
import logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import create_access_token, JWTManager, jwt_required
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#pip install Flask-SQLAlchemy Flask-Migrate

#flask db migrate -m "message"
#flask db upgrade 

logging.basicConfig(level=logging.INFO)
# engine = create_engine('sqlite:///test.db')
# Base = declarative_base()


# Base.metadata.create_all(engine)
# Create a session
# Session = sessionmaker(bind=engine)
# session = Session()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key" 
jwt = JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), nullable=False)
    role = db.Column(String(250), nullable=False)
    age = db.Column(Integer)
    salary = db.Column(Integer)

@app.route("/login", methods=["POST"])
@app.route("/signin", methods=["POST"])
def login():
    usr = request.json.get("usr", None)
    pwd = request.json.get("pwd", None)
    if(usr == "admin" and pwd == "admin"):
        # from datetime import timedelta
        access_token = create_access_token(identity=usr, expires_delta=timedelta(minutes=15))
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401

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
            app.logger.info(f"...input data:{type(new_data)}, val: {new_data}")
            testDict.append(new_data)
            new_person = Person(name = new_data["Name"], role = new_data["Role"], age = 60)
            db.session.add(new_person)
            db.session.commit()
            return make_response(jsonify(testDict), 200)
    except ValidationError as e:
        app.logger.error(f"...validation failed:{e}")
        return make_response(jsonify(e.errors()), 400)    
    return make_response(jsonify(testDict), 200)

@app.route('/oldpersons/<age>',  methods=['GET'])
@jwt_required()
def fetchPersonsAbove(age):
    all_people = session.query(Person).filter(Person.age > age).all()
    results = []
    for p in all_people:
        results.append({"name": p.name, "role": p.role, "age": p.age})
    return jsonify(results) 

@app.route('/persons',  methods=['GET'])
def fetchPersons():
    all_people = session.query(Person).all()
    results = []
    for p in all_people:
        results.append({"name": p.name, "role": p.role, "age": p.age})
    return jsonify(results)

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