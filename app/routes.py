from flask import render_template, make_response, request, redirect, url_for
# from charm.toolbox.pairinggroup import PairingGroup, G1
import requests
import json
import ast

from app import app
from app.src.client import hash_id, deserialize, get_x, serialize

URL = "http://3.108.58.123"

TRUE_VAL = [51, 58, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 69, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65 , 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65 ]

@app.route('/', methods = ['GET', 'POST'])
def index():
    is_correct_pass = True
    if request.cookies.get('token'):
        token = ast.literal_eval(request.cookies.get('token'))
        if token:
            if request.method == 'POST':
                email = request.form['username']
                A = hash_id(email)

                print("token: ", token)
                client_sec = deserialize( token ) + hash_id(request.form['password']) * A
                print("calculated", serialize(client_sec))
                x = get_x()

                U = x * A

                _y = requests.post(
                    f"{URL}/get-y",
                    json = {
                        "id": email,
                        "U_ser": {
                            "__class__": "bytes",
                            "__value__": serialize(U)
                        }
                    }
                )

                y = deserialize(_y.json()["__value__"])
                v = -(x + y) * client_sec

                verify = requests.post(
                    f"{URL}/authenticate",
                    json = {
                        "id": email,
                        "V_ser": {
                            "__class__": "bytes",
                            "__value__": serialize(v)
                        }
                    }
                )

                if verify.json() == TRUE_VAL:
                    print("True")
                    return redirect(url_for("home"))
                else:
                    is_correct_pass = False

        return render_template('login.html', is_correct_pass = is_correct_pass)
    else:
        return redirect(url_for('get_email'))

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/email", methods = ['GET', 'POST'])
def get_email():
    if request.method == 'POST':
        requests.post(
            f"{URL}/otp",
            json = {
                "user_id": request.form['email-id']
            }
        )
        return redirect(url_for('get_otp'))
    return render_template("email.html")

@app.route("/otp", methods = ['GET', 'POST'])
def get_otp():
    is_otp_correct = True
    if request.method == 'POST':
        resp = requests.post(
            f"{URL}/verify",
            json = {
                "user_id": request.form['email'],
                "otp": request.form['otp']
            }
        )
        if resp.json():
            return redirect(url_for('get_pin'))
        else:
            is_otp_correct = False

    return render_template("otp.html", is_otp_correct=is_otp_correct)

@app.route("/pin", methods = ['GET', 'POST'])
def get_pin():
    is_correct = True
    if request.method == 'POST':
        email = request.form['email']
        A = hash_id(email)

        sA = requests.post(
            f"{URL}/client-secret",
            json = {
                "id": email,
                "A_ser": {
                    "__class__": "bytes",
                    "__value__": serialize(A)
                }
            }
        )
        # print("sA from server", sA.json()['__value__'])

        client_sec = deserialize( sA.json()['__value__'] )
        _token = client_sec - hash_id( request.form['new-pin'] ) * A
        token = serialize(_token)
        
        print("sA from server", sA.json()['__value__'],
            "token: ", token,
            "pin: ", int(request.form['new-pin']))
        x = get_x()

        U = x * A

        _y = requests.post(
            f"{URL}/get-y",
            json = {
                "id": email,
                "U_ser": {
                    "__class__": "bytes",
                    "__value__": serialize(U)
                }
            }
        )

        y = deserialize( _y.json()["__value__"] )

        v = -(x + y) * (client_sec)

        verify = requests.post(
            f"{URL}/authenticate",
            json = {
                "id": email,
                "V_ser": {
                    "__class__": "bytes",
                    "__value__": serialize(v)
                }
            }
        )

        if verify.json() == TRUE_VAL:
            print("yea")
            return redirect(url_for('setcookie', token = token))
        else:
            is_correct = False

    return render_template("pin.html", is_correct = is_correct)

@app.route("/setcookie/<token>")
def setcookie(token):
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('token', token)
    return resp

@app.route('/getcookie')
def getcookie():
    uid = request.cookies.get('token')
    return f'cookie: {uid}'

@app.route('/deletecookie')
def deletecookie():
    resp = make_response(f'The Cookie is deleted')
    resp.delete_cookie('token', 'arc')
    return resp
    
