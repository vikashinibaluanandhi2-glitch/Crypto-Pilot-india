from flask import Flask, render_template_string, session, redirect, request
from flask_socketio import SocketIO, emit
import requests
import time

app = Flask(__name__)
app.secret_key = "cryptopilot_vip"
socketio = SocketIO(app, cors_allowed_origins="*")

# ---------------- CACHE (NEW FIX) ----------------
latest_price = 0

# ---------------- LIVE PRICE ----------------
def get_btc():
    global latest_price
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=inr"
        price = requests.get(url, timeout=5).json()["bitcoin"]["inr"]
        latest_price = price
        return price
    except:
        return latest_price   # return last known value (NO ZERO, NO LAG)

# ---------------- BACKGROUND STREAM ----------------
def price_stream():
    while True:
        price = get_btc()
        socketio.emit("price_update", {"btc": price})
        socketio.sleep(3)

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["user"]
        return redirect("/")
    return """
    <h2>CryptoPilot Login</h2>
    <form method='post'>
        <input name='user' placeholder='username'>
        <button>Login</button>
    </form>
    """

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- DASHBOARD ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    # 🔥 NEW FIX: preload value BEFORE page loads
    initial_price = get_btc()

    return render_template_string(HTML,
                                  user=session["user"],
                                  initial_price=initial_price)

# ---------------- UI ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>CryptoPilot India VIP</title>
<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>

<style>
body{
    margin:0;
    font-family:Arial;
    background:#050814;
    color:white;
    overflow:hidden;
}

.bg{
    position:absolute;
    width:100%;
    height:100%;
}

.planet{
    position:absolute;
    border-radius:50%;
    opacity:0.7;
    animation:float 8s ease-in-out infinite;
}

.p1{width:100px;height:100px;background:radial-gradient(circle,#22c55e,#065f46);top:20%;left:70%;}
.p2{width:130px;height:130px;background:radial-gradient(circle,#3b82f6,#1e3a8a);top:60%;left:10%;}
.p3{width:70px;height:70px;background:radial-gradient(circle,#f59e0b,#7c2d12);top:40%;left:40%;}

@keyframes float{
    0%{transform:translateY(0);}
    50%{transform:translateY(-25px);}
    100%{transform:translateY(0);}
}

.sidebar{
    position:fixed;
    width:260px;
    height:100vh;
    background:rgba(15,23,42,0.9);
    padding:20px;
}

.logo{
    font-size:22px;
    color:#22c55e;
    text-align:center;
    font-weight:bold;
}

.menu div{
    background:#111827;
    padding:12px;
    margin:10px 0;
    border-radius:10px;
}

.main{
    margin-left:280px;
    padding:20px;
}

.title{
    font-size:30px;
    color:#22c55e;
    font-weight:bold;
}

.price{
    font-size:50px;
    color:#22c55e;
    text-shadow:0 0 15px #22c55e;
}
</style>
</head>

<body>

<div class="bg">
<div class="planet p1"></div>
<div class="planet p2"></div>
<div class="planet p3"></div>
</div>

<div class="sidebar">
<div class="logo">CryptoPilot VIP 🚀</div>
<div class="menu">
<div>Dashboard</div>
<div>Markets</div>
<div>Portfolio</div>
<div>Wallet</div>
<div>Settings</div>
</div>
</div>

<div class="main">
<div class="title">Welcome {{user}}</div>

<h2>Bitcoin Live (REAL TIME)</h2>

<!-- 🔥 FIX: show initial price immediately -->
<div class="price" id="btc">₹ {{initial_price}}</div>
</div>

<script>
var socket = io();

/* real-time updates */
socket.on("price_update", function(data){
    document.getElementById("btc").innerText =
        "₹ " + data.btc.toLocaleString();
});
</script>

</body>
</html>
"""

# ---------------- SOCKET ----------------
@socketio.on("connect")
def connect():
    # 🔥 FIX: send instant value on connect (no lag)
    emit("price_update", {"btc": latest_price})

# start stream
socketio.start_background_task(price_stream)

# ---------------- RUN ----------------
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
