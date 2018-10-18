from flask import Flask, session, request, render_template, redirect, url_for, jsonify
from flask_session import Session
import random, string

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
print(app.secret_key)

global nickname_list, rooms_list
nickname_list = []
rooms_list = ["General", "Room_first", "Test_room"]
last_room = {}

@app.route('/')
def home():
    return render_template("index.html", room_now="General", rooms_list=rooms_list)


@app.route('/login', methods=['POST'])
def do_admin_login():
    nickname = request.form["nickname"]
    if nickname in nickname_list:
        return render_template("index.html", info_type="error", info_text="This user already exist!")
    else:
        session['logged_in'] = True
        session["nickname"] = nickname
        nickname_list.append(nickname)
        return render_template("index.html", info_type="succes", info_text=f"You are logged as {nickname}", room_now="General", rooms_list=rooms_list)


@app.route("/logout")
def logout():
    if session.get('logged_in'):

        # In case there was a server restart when user is still logged in and - in this case - his nickname is not in the list anymore (list of nicknames is stored only when SERVER IS WORKING)
        # In this case, we trust that user is not manipulating cookies, but still - we don't check that nick is associated with the same person whatsoever...
        if session["nickname"] in nickname_list:
            nickname_list.remove(session["nickname"])

        session.clear()
        print("Left users:", nickname_list)
        return render_template("index.html", info_type="neutral", info_text="Hope to see you soon! :)")
    else:
        return redirect(url_for('home'))


@app.route("/room/<roomname>")
def gotoroom(roomname):
    return render_template("index.html", room_now=roomname, rooms_list=rooms_list)


if __name__ == '__main__':
    app.run()
