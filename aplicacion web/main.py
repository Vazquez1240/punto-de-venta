from flask import redirect, url_for, render_template, flash, Flask,request
from flask.globals import session
import requests
import json

app = Flask(__name__)

API_WEB_USER = "http://localhost:8000/user"
API_WEB_ADMIN = "http://localhost:8000/"
API_WEB_LOGIN = 'http://localhost:8000/auth'
API_WEB_LOGOUT = 'http://localhost:8000/logout'

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
        grant_type = 'password'
        user = {
            "username":username,
            "password":password
        }
        print(user)
        response = requests.post(API_WEB_LOGIN+"/",data={'username':username,'password':password})
        print(response)
        if(response.status_code == 200):
            session["usuario"] = True
            token = response.json()["access_token"]
            
            return render_template('inicio.html',username=user["username"],session=session["usuario"],token=token)
        else:
            return "error"
    if(request.method == "GET"):
        username = request.form["username"]
        password = request.form["password"]
        grant_type = 'password'
        user = {
            "username":username,
            "password":password
        }
        print(user)
        response = requests.post(API_WEB_LOGIN+"/",data={'username':username,'password':password})
        print(response)
        if(response.status_code == 200):
            session["usuario"] = True
            token = response.json()["access_token"]
            
            return render_template('inicio.html',username=user["username"],session=session["usuario"],token=token)
        else:
            return "error"
        
@app.route("/logout/<token>/<username>")
def logout(token,username):
    token_session = token
    response = requests.delete(API_WEB_LOGOUT+'/', params={"token":token_session,'username':username})
    print(response)
    if response.status_code == 202:
        # Lógica para eliminar el token de sesión de la sesión de Flask
        return redirect(url_for('home'))
    else:
        return "Error al cerrar la sesión"

if(__name__ == '__main__'):
    app.run(debug=True,port="5000",host="0.0.0.0")