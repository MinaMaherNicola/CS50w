import os

from flask import Flask, session, redirect, render_template, request, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "putSecretKeyHere"
socketio = SocketIO(app)

# To list all the users
usernames = []

# To list all the expenses and incomes description
expenses = []
incomes = []

# To list all the expenses values and incomes values
expensesValue = []
incomesValue = []

# To list all the total values
totalBudget = []
totalIncomesValue = []
totalExpensesValue = []


@app.route("/")
def index():
    global usernames
    # if the user is already logged in go to budget and display his totals
    if len(usernames) > 0:
        return redirect("/budget")
    # else go to index page
    else:
        return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        global usernames, expensesValue, expenses, incomesValue, incomes, totalBudget, totalIncomesValue, totalExpensesValue

        session["username"] = request.form.get("username")
        session.permanent = True
        usernames.append(session["username"])
        session["userID"] = usernames.index(session["username"])
        session.permanent = True
        # append total budget
        totalBudget.append(0)
        # append total incomes
        totalIncomesValue.append(0)
        # append total expenses
        totalExpensesValue.append(0)
        # append incomes
        incomes.append([])
        # append expenses
        expenses.append([])
        # append incomes value
        incomesValue.append([])
        # append expenses value
        expensesValue.append([])
        return redirect("/budget")
        
    else:
        return redirect("/")

@app.route("/budget")
def budget():
    if session["username"]:
        return render_template("budget.html", username=session["username"], totalBudget=totalBudget[session["userID"]], totalIncome=totalIncomesValue[session["userID"]], totalExpense=totalExpensesValue[session["userID"]], incomes=incomes[session["userID"]], incomesValue=incomesValue[session["userID"]], expenses=expenses[session["userID"]], expensesValue=expensesValue[session["userID"]])
    else:
        return redirect("/")


@socketio.on("add income")
def addIncome(income):
    global incomesValue, incomes, totalBudget, totalIncomesValue, totalExpensesValue

    incomes[session["userID"]].append(income["description"])

    incomesValue[session["userID"]].append(float(income["value"]))

    totalIncomesValue[session["userID"]] += float(income["value"])

    totalBudget[session["userID"]] = totalIncomesValue[session["userID"]] - totalExpensesValue[session["userID"]]

    socketio.emit("show income", {"description": income["description"], "value": income["value"], "id": len(incomes) - 1, "totalIncome": totalIncomesValue, "totalBudget": totalBudget})

@socketio.on("add expense")
def addExpense(expense):
    global expensesValue, expenses, totalBudget, totalExpensesValue, totalIncomesValue
    expenses[session["userID"]].append(expense["description"])
    expensesValue[session["userID"]].append(float(expense["value"]))
    totalExpensesValue[session["userID"]] += float(expense["value"])
    totalBudget[session["userID"]] = totalIncomesValue[session["userID"]] - totalExpensesValue[session["userID"]]
    socketio.emit("show expense", {"description": expense["description"], "value": expense["value"], "id": len(expenses) - 1, "totalExpense": totalExpensesValue, "totalBudget": totalBudget})

@socketio.on("remove income")
def removeIncome(number):
    global incomesValue, incomes, totalBudget, totalIncomesValue
    index = int(number["index"]) - 1
    # Subtract the income value from totals
    incomes[session["userID"]].pop(index)
    removedValue = incomesValue[session["userID"]][index]
    incomesValue[session["userID"]].pop(index)
    totalBudget[session["userID"]] -= removedValue
    totalIncomesValue[session["userID"]] -= removedValue

    socketio.emit("show income", {"totalIncome": totalIncomesValue, "totalBudget": totalBudget})

@socketio.on("remove expense")
def removeExpense(number):
    global expensesValue, expenses, totalBudget, totalExpensesValue
    index = int(number["index"]) - 1
    # Add value to total budget and subtract it from expense total
    expenses[session["userID"]].pop(index)
    removedValue = expensesValue[session["userID"]][index]
    expensesValue[session["userID"]].pop(index)
    totalBudget[session["userID"]] += removedValue
    totalExpensesValue[session["userID"]] -= removedValue

    socketio.emit("show expense", {"totalExpense": totalExpensesValue, "totalBudget": totalBudget})    