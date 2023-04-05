from flask import redirect, url_for, render_template, flash, Flask,request
from flask.globals import session
import requests


app = Flask(__name__)

API_WEB_USER = "http://localhost:8000/user"
API_WEB_ADMIN = "http://localhost:8000/admin"
API_WEB_LOGIN = 'http://localhost:8000/auth'

app.secret_key = "adbcdefg23533@!#-$3$!EDFw"



@app.route("/")
def home():
    response = requests.get(API_WEB_ADMIN+"/obtener_admins")
    data = response.json()
    return render_template('index.html')



@app.route("/logeo", methods=["POST","GET"])
def loge():
    if(request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]
        
        user = {
            "username":username,
            "password":password
        }
        print(user)
        response = requests.post(API_WEB_LOGIN+"/token",json=user)
        print(response)
        if(response.status_code == 200):
            session["usuario"] = True
            return render_template('inicio.html',username=user["username"],session=session["usuario"])
        else:
            return "error"
        



if(__name__ == '__main__'):
    app.run(debug=True,host='0.0.0.0',port="5000")