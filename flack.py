from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)

nickname_list = []
rooms_list = ["General", "Room_first"]
# TODO unify getting rooms_list from message_list
messages_list = {"General":
                     [[1, "admin", "This is first message, that appears with timestamp of one"],
                      [2, "admin", "This is second message, that appears with timestamp of two"],
                      [3, "admin", "This is third message, that appears with timestamp of three"]], "Room_first": []}

app.jinja_env.globals['messages_list'] = messages_list
# TODO add all stuff from render_template to free all return render_template from repeated parameters


@app.route('/')
def home():
    if session.get("logged_in"):
        return render_template("room.html", room_now=session["last_room"], rooms_list=rooms_list, nickname=session["nickname"])
    else:
        return render_template("index.html", rooms_list=rooms_list)


@app.route('/login', methods=['POST'])
def do_admin_login():
    nickname = request.form["nickname"]
    if nickname in nickname_list:
        return render_template("index.html", info_type="error", info_text="This user already exist!")
    else:
        session['logged_in'] = True
        session["nickname"] = nickname
        nickname_list.append(nickname)
        print(f"{nickname} logged in :)")
        return redirect(url_for('gotoroom', roomname="General"))


@app.route("/logout")
def logout():
    if session.get('logged_in'):

        # In case there was a server restart when user is still logged in and - in this case - his nickname is not in the list anymore (list of nicknames is stored only when SERVER IS WORKING)
        # In this case, we trust that user is not manipulating cookies, but still - we don't check that nick is associated with the same person whatsoever...
        exituser = session["nickname"]
        if session["nickname"] in nickname_list:
            nickname_list.remove(session["nickname"])

        session.clear()
        print(f"{exituser} logged out :(")
        return render_template("index.html", info_type="neutral", info_text="Hope to see you soon! :)", rooms_list=rooms_list)
    else:
        return redirect(url_for('home'))


@app.route("/room/<roomname>")
def gotoroom(roomname):
    if session.get('logged_in'):
        session["last_room"] = roomname
        if roomname in rooms_list:
            return render_template("room.html", room_now=roomname, rooms_list=rooms_list, nickname=session["nickname"])
        else:
            return render_template("room.html", info_type="error", info_text="Room doesn't exits! Redirect to: General", nickname=session["nickname"], rooms_list=rooms_list, room_now="General")
    else:
        return render_template("index.html", info_type="error", info_text="You must first choose nickname!")


@app.route("/new_room", methods=['POST'])
def new_room():
    if session.get('logged_in'):
        new_room_name = request.form["new_room_name"]

        return redirect(url_for('gotoroom', roomname=new_room_name))
    else:
        return render_template("index.html", info_type="error", info_text="You must first choose nickname!")


@socketio.on("update_room_list")
def add_room(new_room_name):
    if not new_room_name in rooms_list:
        rooms_list.append(new_room_name)
        messages_list.update({new_room_name: {}})
        emit("Update room list", new_room_name, broadcast=True)
        print(f"NOWY POKÓJ {new_room_name}")
    else:
        render_template("index.html", info_type="error", info_text="This room exist!")


@socketio.on("new_message_submit")
def add_message(new_message_body):
    messages_list_in_room = messages_list[session["last_room"]]

    messages_list_in_room.update({"author": session["nickname"], "datetime": time.time(), "message": new_message_body})
    # TODO repair parsing json for JS

    messages_list_in_room = sorted(messages_list_in_room[session["last_room"]])

    emit("update_messages", messages_list_in_room, broadcast=True)
    print(f"NOWA WIADOMOŚĆ {new_message_body} w pokoju {room}")


if __name__ == '__main__':
    app.run()
