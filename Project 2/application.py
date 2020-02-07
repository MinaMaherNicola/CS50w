import os

from flask import Flask, request, render_template, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "PutSecretKeyHere"
socketio = SocketIO(app)

#Global Vars
usersLogged = []
channelsList = []
messages = []
idHolder = -1    

@app.route("/")
def index():
    if usersLogged:
        if session["channel_id"] != -1:
            return render_template("channel.html", displayName=usersLogged[session["user_id"]], messages=messages[session["channel_id"]])
        else:
            return render_template("channelslist.html", displayName=usersLogged[session["user_id"]], channelsList=channelsList)
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    global usersLogged
    if request.method == "POST":
        displayName = request.form.get("displayName")
        if displayName == "":
            return render_template("error.html", e="Please provide a username")
        elif displayName in usersLogged:
            return render_template("error.html", e="User already exists please enter another username")
        else:
            session["username"] = displayName
            session.permanent = True
            usersLogged.append(displayName)
            # FLAG
            index = usersLogged.index(displayName)
            session["user_id"] = index
            session.permanent = True
            session["channel_id"] = -1
            session.permanent = True
            return render_template("channelslist.html", displayName=usersLogged[session["user_id"]], channelsList=channelsList)
    else: 
        return render_template("index.html")

@app.route("/logout")
def logout():
    usersLogged.pop(session["user_id"])
    session.clear()
    return render_template("index.html")

@app.route("/channels")
def channels():
    if not session["username"]:
        return render_template("index.html")
    else:
        session["channel_id"] = -1
        # session.permanent = True
        return render_template("channelslist.html", displayName=usersLogged[session["user_id"]], channelsList=channelsList)

@app.route("/createChannel", methods=["POST"])
def createChannel():
    global channelsList
    global messages
    newChannelName = request.form.get('createChannelName')
    session["channel_id"] = -1
    # session.permanent = True
    if not newChannelName:
        return render_template("error.html", e="Please provide a valid channel name")
    elif newChannelName in channelsList:
        return render_template("error.html", e="Channel name already exist please provide other name.")
    else:
        channelsList.append(newChannelName)
        messages.append([])
        return render_template("channelslist.html", displayName=usersLogged[session["user_id"]], channelsList=channelsList)

@app.route("/channel")
def channel():
    global messages
    global idHolder
    global channelsList
    session["channel_id"] = idHolder
    session.permanent = True
    title = channelsList[session["channel_id"]]
    if len(messages[session["channel_id"]]):
        holder = len(messages[session["channel_id"]])
        holder -= 100
        del messages[session["channel_id"]][0:holder]
    return render_template("channel.html", displayName=usersLogged[session["user_id"]], messages=messages[session["channel_id"]], name=title)

@socketio.on("channel id")
def channelID(data):
    global idHolder
    idHolder = int(data["index"]) - 1
     
    

@socketio.on("send message")
def sendMsg(data):
    global messages
    wholeMessage = session["username"] + ": " + data["message"] + " <" + data["time"] + ">"
    messages[session["channel_id"]].append(wholeMessage)
    emit("print msg", {"msg": wholeMessage}, broadcast=True)


@socketio.on("delete channel")
def deleteChannel(data):
    global messages
    global idHolder
    global channelsList
    idHolder = int(data["index"])
    idHolder -= 1
    messages.pop(idHolder)
    channelsList.pop(idHolder)