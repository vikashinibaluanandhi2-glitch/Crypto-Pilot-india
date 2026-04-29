from flask import Flask, request, redirect, session, jsonify
import urllib.request, json, sqlite3

app = Flask(__name__)
app.secret_key = "cryptopilot_secure_key"

# ===== DATABASE SETUP =====
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        balance REAL DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ===== FETCH LIVE CRYPTO DATA (INR + CHANGE) =====
def get_crypto():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data[:6]
    except:
        return []

# ===== LANDING PAGE =====
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>CryptoPilot India</title>
<meta name="viewport" content="width=device-width">

<style>
body{
    margin:0;
    font-family:Segoe UI;
    background:linear-gradient(135deg,#0B0F1A,#111827);
    color:white;
}

/* HERO */
.hero{
    text-align:center;
    padding:80px 20px;
}
.hero h1{
    font-size:42px;
}
.hero span{
    color:#6366F1;
}

/* STATS */
.stats{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
}
.card{
    background:rgba(255,255,255,0.05);
    padding:20px;
    margin:10px;
    border-radius:12px;
    width:260px;
}

/* LOGIN */
.login{
    text-align:center;
    padding:60px;
}
input{
    padding:10px;
    margin:8px;
    border-radius:6px;
    border:none;
}
button{
    padding:10px 20px;
    background:#6366F1;
    border:none;
    color:white;
    border-radius:6px;
}
</style>
</head>

<body>

<div class="hero">
<h1>Future of <span>AI Crypto</span></h1>
<p>Track, Analyze & Learn Crypto in ₹ (India)</p>
</div>

<div class="stats" id="stats"></div>

<div class="login">
<h2>Login / Signup</h2>

<form method="POST" action="/login">
<input name="username" placeholder="Username" required><br>
<input name="password" type="password" placeholder="Password" required><br>
<button>Login</button>
</form>

<br>

<form method="POST" action="/signup">
<input name="username" placeholder="New Username" required><br>
<input name="password" type="password" placeholder="New Password" required><br>
<button>Create Account</button>
</form>
</div>

<script>
async function load(){
    let res = await fetch("/data");
    let data = await res.json();

    let html = "";

    data.forEach(c=>{
        let change = c.price_change_percentage_24h.toFixed(2);

        html += `
        <div class="card">
        <h3>${c.name}</h3>
        <p>Today: ₹ ${c.current_price}</p>
        <p style="color:${change>=0?'#00ff99':'#ff4d4d'}">
        24h: ${change}%
        </p>
        </div>
        `;
    });

    document.getElementById("stats").innerHTML = html;
}

load();
setInterval(load,60000);
</script>

</body>
</html>
"""

# ===== SIGNUP =====
@app.route("/signup", methods=["POST"])
def signup():
    u = request.form["username"]
    p = request.form["password"]

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (?,?,?)",(u,p,0))
        conn.commit()
    except:
        conn.close()
        return "<h3 style='color:red'>Username already exists</h3>"

    conn.close()
    return redirect("/")

# ===== LOGIN =====
@app.route("/login", methods=["POST"])
def login():
    u = request.form["username"]
    p = request.form["password"]

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
    user = c.fetchone()
    conn.close()

    if user:
        session["user"] = u
        return redirect("/dashboard")

    return "<h3 style='color:red'>Invalid Username or Password</h3>"

# ===== DASHBOARD =====
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width">
<style>
body{
    background:#0B0F1A;
    color:white;
    font-family:Segoe UI;
}
.card{
    background:#111827;
    padding:15px;
    margin:10px;
    border-radius:10px;
}
input{
    padding:10px;
    margin:5px;
}
button{
    padding:10px;
    background:#6366F1;
    color:white;
    border:none;
}
</style>
</head>

<body>

<h2>CryptoPilot Dashboard 🚀</h2>

<div class="card">
<h3>Your Wallet</h3>
<p id="balance">₹0</p>
<input id="amt" placeholder="Enter ₹">
<button onclick="add()">Add</button>
<button onclick="remove()">Withdraw</button>
</div>

<div class="card">
<h3>Convert ₹ → Bitcoin</h3>
<input id="convertAmt" placeholder="Enter ₹">
<button onclick="convert()">Convert</button>
<p id="result"></p>
</div>

<div class="card">
<h3>Live Crypto Prices</h3>
<div id="list"></div>
</div>

<a href="/logout"><button>Logout</button></a>

<script>
async function load(){
    let res=await fetch("/data");
    let data=await res.json();

    let html="";
    data.forEach(c=>{
        html+=`<p>${c.name}: ₹ ${c.current_price}</p>`;
    });

    document.getElementById("list").innerHTML=html;
}

async function getBalance(){
    let r=await fetch("/balance");
    let d=await r.json();
    document.getElementById("balance").innerText="₹ "+d.balance;
}

async function add(){
    let v=document.getElementById("amt").value;
    await fetch("/add?amt="+v);
    getBalance();
}

async function remove(){
    let v=document.getElementById("amt").value;
    await fetch("/remove?amt="+v);
    getBalance();
}

async function convert(){
    let amt=document.getElementById("convertAmt").value;
    let res=await fetch("/data");
    let data=await res.json();

    let btc=data[0].current_price;
    let result=(amt/btc).toFixed(6);

    document.getElementById("result").innerText =
    amt + " INR = " + result + " BTC";
}

load();
getBalance();
setInterval(load,60000);
</script>

</body>
</html>
"""

# ===== APIs =====
@app.route("/data")
def data():
    return jsonify(get_crypto())

@app.route("/balance")
def balance():
    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("SELECT balance FROM users WHERE username=?", (session["user"],))
    bal=c.fetchone()[0]
    conn.close()
    return jsonify({"balance":bal})

@app.route("/add")
def add():
    amt=float(request.args.get("amt",0))
    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("UPDATE users SET balance=balance+? WHERE username=?", (amt,session["user"]))
    conn.commit()
    conn.close()
    return "ok"

@app.route("/remove")
def remove():
    amt=float(request.args.get("amt",0))
    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("SELECT balance FROM users WHERE username=?", (session["user"],))
    bal=c.fetchone()[0]

    if bal >= amt:
        c.execute("UPDATE users SET balance=balance-? WHERE username=?", (amt,session["user"]))
        conn.commit()

    conn.close()
    return "ok"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()
    
