from flask import Flask, request, redirect, session, jsonify
import urllib.request, json, sqlite3

app = Flask(__name__)
app.secret_key = "secret"

# ===== DATABASE =====
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, balance REAL)")
    conn.commit()
    conn.close()

init_db()

# ===== CRYPTO =====
def get_crypto():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr"
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
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body{
    margin:0;
    font-family:Segoe UI;
    background:linear-gradient(135deg,#0B0F1A,#111827);
    color:white;
}

/* NAV */
.nav{
    padding:15px;
    display:flex;
    justify-content:space-between;
}
.logo{
    color:#6366F1;
    font-weight:bold;
}
.btn{
    background:#6366F1;
    padding:8px 15px;
    border-radius:6px;
    color:white;
    text-decoration:none;
}

/* HERO */
.hero{
    text-align:center;
    padding:80px 20px;
}
.hero h1{
    font-size:40px;
}
.hero span{
    color:#6366F1;
}

/* SECTION */
.section{
    padding:50px 20px;
    text-align:center;
}
.card{
    background:rgba(255,255,255,0.05);
    padding:20px;
    margin:15px;
    border-radius:12px;
}

/* LOGIN */
.login{
    padding:50px;
    text-align:center;
}
input{
    padding:10px;
    width:250px;
    margin:10px;
    border:none;
    border-radius:6px;
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

<div class="nav">
<div class="logo">CryptoPilot India 🚀</div>
<a href="#login" class="btn">Login</a>
</div>

<div class="hero">
<h1>Future of <span>AI Crypto</span> in India</h1>
<p>Track, Predict & Grow your crypto portfolio in ₹</p>
</div>

<div class="section">
<h2>Why CryptoPilot?</h2>
<div class="card">📊 Live Crypto Prices (₹)</div>
<div class="card">🤖 AI Predictions</div>
<div class="card">🔐 Secure Portfolio</div>
</div>

<div class="section">
<h2>Built for India 🇮🇳</h2>
<div class="card">All values in INR ₹</div>
<div class="card">Simple UI anyone can use</div>
</div>

<div id="login" class="login">
<h2>Login / Signup</h2>

<form method="POST" action="/login">
<input name="username" placeholder="Username"><br>
<input name="password" type="password" placeholder="Password"><br>
<button>Login</button>
</form>

<br>

<form method="POST" action="/signup">
<input name="username" placeholder="New Username"><br>
<input name="password" type="password" placeholder="New Password"><br>
<button>Create Account</button>
</form>

</div>

</body>
</html>
"""

# ===== LOGIN =====
@app.route("/login", methods=["POST"])
def login():
    u=request.form["username"]
    p=request.form["password"]

    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))
    user=c.fetchone()
    conn.close()

    if user:
        session["user"]=u
        return redirect("/dashboard")

    return "Invalid Login"

# ===== SIGNUP =====
@app.route("/signup", methods=["POST"])
def signup():
    u=request.form["username"]
    p=request.form["password"]

    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?,?)",(u,p,0))
    conn.commit()
    conn.close()

    return redirect("/")

# ===== DASHBOARD =====
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return """
    <h2>Welcome to CryptoPilot India 🚀</h2>
    <a href="/logout">Logout</a>
    <div id="data"></div>

    <script>
    async function load(){
        let res=await fetch("/data");
        let data=await res.json();
        let html="";
        data.forEach(c=>{
            html+=`<p>${c.name} ₹ ${c.current_price}</p>`;
        });
        document.getElementById("data").innerHTML=html;
    }
    load();
    </script>
    """

# ===== DATA =====
@app.route("/data")
def data():
    return jsonify(get_crypto())

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run()
