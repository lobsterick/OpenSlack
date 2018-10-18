from flask import Flask, session, request, render_template, redirect, url_for, jsonify
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

global nickname_list, rooms_list
nickname_list = []
rooms_list = ["General"]


@app.route('/')
def index_page():
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
        return render_template("index.html", info_type="succes", info_text= f"You are logged as {nickname}")


@app.route("/logout")
def logout():
    if session.get('logged_in'):
        nickname_list.remove(session["nickname"])
        session['logged_in'] = False
        return render_template("index.html", info_type="neutral", info_text="Hope to see you soon! :)")
    else:
        return redirect(url_for('home'))















if __name__ == '__main__':
    app.run()
