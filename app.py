from flask import Flask, request, redirect, session, jsonify
import urllib.request, json

app = Flask(__name__)
app.secret_key = "secret123"   # change later

# ===== SIMPLE DATABASE (temporary) =====
users = {}

# ===== GET CRYPTO =====
def get_crypto():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data[:10]
    except:
        return []

# ===== LOGIN PAGE =====
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect("/dashboard")

        return "Invalid login"

    return """
    <h2>Login</h2>
    <form method="POST">
        <input name="username" placeholder="Username" required><br><br>
        <input name="password" type="password" placeholder="Password" required><br><br>
        <button>Login</button>
    </form>
    <a href="/signup">Create Account</a>
    """

# ===== SIGNUP =====
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return "User already exists"

        users[username] = {"password": password, "balance": 0}
        return redirect("/")

    return """
    <h2>Signup</h2>
    <form method="POST">
        <input name="username" placeholder="Username" required><br><br>
        <input name="password" type="password" required><br><br>
        <button>Create</button>
    </form>
    """

# ===== DASHBOARD =====
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return """
<!DOCTYPE html>
<html>
<head>
<title>CryptoPilot India</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
body {background:#0B0F1A;color:white;font-family:Arial;}
.card {background:#111827;padding:15px;margin:10px;border-radius:10px;}
button {background:#6366F1;color:white;border:none;padding:10px;}
</style>
</head>

<body>

<h2>CryptoPilot India 🚀</h2>
<a href="/logout">Logout</a>

<div class="card">
<h3>Balance</h3>
<p id="balance">₹ 0</p>
<input id="amt" placeholder="Enter ₹">
<button onclick="add()">Add</button>
<button onclick="remove()">Withdraw</button>
</div>

<div class="card">
<h3>Crypto</h3>
<div id="list"></div>
</div>

<div class="card">
<h3>Chart</h3>
<canvas id="chart"></canvas>
</div>

<script>
let chart;

async function load(){
    let res = await fetch("/data");
    let data = await res.json();

    let html="";
    let labels=[];
    let prices=[];

    data.forEach(c=>{
        html+=`<p>${c.name} ₹ ${c.current_price}</p>`;
        labels.push(c.name);
        prices.push(c.current_price);
    });

    document.getElementById("list").innerHTML=html;

    if(chart) chart.destroy();

    chart=new Chart(document.getElementById("chart"),{
        type:"bar",
        data:{labels:labels,datasets:[{data:prices}]}
    });
}

async function add(){
    let val=document.getElementById("amt").value;
    await fetch("/add?amt="+val);
    getBalance();
}

async function remove(){
    let val=document.getElementById("amt").value;
    await fetch("/remove?amt="+val);
    getBalance();
}

async function getBalance(){
    let res=await fetch("/balance");
    let data=await res.json();
    document.getElementById("balance").innerText="₹ "+data.balance;
}

load();
getBalance();
setInterval(load,60000);
</script>

</body>
</html>
"""

# ===== BALANCE API =====
@app.route("/balance")
def balance():
    user = session.get("user")
    return jsonify({"balance": users[user]["balance"]})

@app.route("/add")
def add():
    user = session.get("user")
    amt = float(request.args.get("amt", 0))
    users[user]["balance"] += amt
    return "ok"

@app.route("/remove")
def remove():
    user = session.get("user")
    amt = float(request.args.get("amt", 0))
    if users[user]["balance"] >= amt:
        users[user]["balance"] -= amt
    return "ok"

# ===== DATA =====
@app.route("/data")
def data():
    return jsonify(get_crypto())

# ===== LOGOUT =====
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()
