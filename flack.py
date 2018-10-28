from flask import Flask, session, request, render_template, redirect, url_for, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit
import time, re

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)

nickname_list = []
messages_list = dict(General=[[1, "admin", "This is first message, that appears with timestamp of one"],
                              [2, "admin", "This is second message, that appears with timestamp of two"],
                              [3, "admin", "This is third message - timestamp of three"]])

rooms_list = list(messages_list.keys())


app.jinja_env.globals['messages_list'] = messages_list
app.jinja_env.globals['rooms_list'] = rooms_list


@app.route('/')
def home():
    if session.get("logged_in"):
        return redirect(url_for('go_to_room', roomname=session["last_room"]))
    else:
        return render_template("index.html")


@app.route('/login', methods=['POST'])
def do_admin_login():
    nickname = request.form["nickname"]
    if nickname in nickname_list:
        return render_template("index.html", info_type="error", info_text="This user already exist!")
    else:
        session['logged_in'] = True
        session["nickname"] = nickname
        nickname_list.append(nickname)
        return redirect(url_for('go_to_room', roomname="General"))


@app.route('/checklogin', methods=['POST', 'GET'])
def check_login():
    if request.method == 'POST':
        print("POST method on /checklogin")
        requested_nickname = str(request.form['nickname'])
        requested_last_room = str(request.form['last_room'])
        if session.get("logged_in") and session.get("nickname") and session["nickname"] == requested_nickname:
            print("User is properly using website")
            return jsonify({"status": True, "last_room": session["last_room"]})
        elif requested_nickname in nickname_list:
            session["logged_in"] = True
            session["nickname"] = requested_nickname
            session["last_room"] = requested_last_room
            print("User has localStorage that is consistent with server data")
            return jsonify({"status": False})
        else:
            nickname_list.append(requested_nickname)
            session["logged_in"] = True
            session["nickname"] = requested_nickname
            session["last_room"] = requested_last_room
            print("User has localStorage that INCONSISTENT with server data, but now he is logged in. It may be caused by server restart.")
            return jsonify({"status": False})

    if request.method == 'GET':
        print("GET method on /checklogin")
        if session.get("logged_in"):
            response = {"logged": True, "nickname": session["nickname"], "last_room": session["last_room"]}
            print("Responded with True")
            return jsonify(response)
        else:
            print("Responded with False")
            response = {"logged": False}
            return jsonify(response)


@app.route("/logout")
def logout():
    if session.get('logged_in'):
        if session["nickname"] in nickname_list:
            nickname_list.remove(session["nickname"])
        else:
            print("There is a possibility that more than one person was using the same nickname in the same time")
        session.clear()
        return render_template("index.html", info_type="neutral", info_text="Hope to see you soon! :)", logout=True)
    else:
        return redirect(url_for('home'))


@app.route("/room/<roomname>")
def go_to_room(roomname):
    if session.get('logged_in'):
        session["last_room"] = roomname
        if roomname in rooms_list:
            return render_template("room.html")
        else:
            return redirect(url_for('go_to_room', roomname="General"))
    else:
        return render_template("index.html", info_type="error", info_text="You must first choose nickname!")


@app.route("/room/<roomname>/json", methods=['GET'])  # endpoint for fetching posts when entering room
def get_room_messages(roomname):
    if session.get('logged_in'):
        if roomname in rooms_list:
            messages_list_last_100 = messages_list[roomname][-100:]
            updated_list = {"success": True, roomname: messages_list_last_100}
            return jsonify(updated_list)
    else:
        return jsonify({"success": False})


@app.route("/new_room", methods=['POST'])  # logic of making new room in socketio.on("update_room_list")
def new_room():
    if session.get('logged_in'):
        new_room_name_requested = request.form["new_room_name"]
        new_room_name = re.sub('[^0-9a-zA-Z]+', "", new_room_name_requested)  # sanitizing
        if new_room_name != "":
            return redirect(url_for('go_to_room', roomname=new_room_name))
        else:
            return redirect(url_for('go_to_room', roomname="General"))

    else:
        return render_template("index.html", info_type="error", info_text="You must first choose nickname!")


@socketio.on("update_room_list")  # sanitized with JS side, but can be sanitized here like new_room()
def add_room(new_room_name):
    if new_room_name not in rooms_list:
        rooms_list.append(new_room_name)
        messages_list.update({new_room_name: []})
        emit("Update room list", new_room_name, broadcast=True)


@socketio.on("new_message_submit")
def add_message(new_message_body):
    messages_list[session["last_room"]].append([time.time(), session["nickname"], new_message_body])
    messages_list[session["last_room"]] = messages_list[session["last_room"]][-100:]
    messages_list_last_100 = messages_list[session["last_room"]]
    updated_list = {session["last_room"]: messages_list_last_100}
    emit("update_messages", updated_list, broadcast=True)


@app.route("/add100")  # for research purposes :)
def add_room(messages_list, rooms_list):
    for room in rooms_list:
        for message in range(100):
            new_message_body = f"This is automatic message number {message+1}"
            messages_list[room].append([time.time(), "AutomatMessages", new_message_body])
    return redirect(url_for('go_to_room', roomname="General"))


@app.route("/deleteall")  # delete all message and log out
def delete_all_messages():
    global messages_list, nickname_list
    if session.get('logged_in'):
        user = session["nickname"]
        messages_list_new = {}

        for room in messages_list:
            messages_list_new.update({room: []})
            for item in messages_list[room]:
                if item[1] != user:
                    messages_list_new[room].append(item)

        messages_list = messages_list_new

        if session["nickname"] in nickname_list:
            nickname_list.remove(session["nickname"])
        session.clear()
        return render_template("index.html", info_type="neutral", info_text="All your data and posts have been deleted. Hope to see you again! :(", logout=True)
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()