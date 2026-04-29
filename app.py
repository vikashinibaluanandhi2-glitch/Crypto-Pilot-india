from flask import Flask, render_template_string, session, redirect, request
from flask_socketio import SocketIO, emit
import requests
import os
import threading
import time

app = Flask(__name__)
app.secret_key = "cryptopilot_vip"

# ✅ SAFE MODE (BEST FOR RENDER FREE DEPLOY)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

latest_price = 0

# ---------------- PRICE ----------------
def get_btc():
    global latest_price
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=inr"
        price = requests.get(url, timeout=5).json()["bitcoin"]["inr"]
        latest_price = price
        return price
    except:
        return latest_price


# ---------------- BACKGROUND STREAM (SAFE THREAD) ----------------
def stream():
    global latest_price
    time.sleep(2)  # allow server to start first

    while True:
        price = get_btc()
        socketio.emit("price_update", {"btc": price})
        time.sleep(3)


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


# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    return render_template_string(HTML,
        user=session["user"],
        initial_price=get_btc()
    )


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
}

.main{
    margin-left:280px;
    padding:20px;
}

.price{
    font-size:50px;
    color:#22c55e;
    text-shadow:0 0 15px #22c55e;
}
</style>
</head>

<body>

<div class="main">
<h2>Welcome {{user}}</h2>

<h2>Bitcoin Live Price</h2>

<div class="price" id="btc">₹ {{initial_price}}</div>
</div>

<script>
var socket = io();

socket.on("price_update", function(data){
    document.getElementById("btc").innerText =
        "₹ " + data.btc.toLocaleString();
});
</script>

</body>
</html>
"""


# ---------------- START BACKGROUND SAFELY ----------------
def start_background():
    thread = threading.Thread(target=stream)
    thread.daemon = True
    thread.start()


@socketio.on("connect")
def connect():
    emit("price_update", {"btc": get_btc()})


# ---------------- RUN ----------------
if __name__ == "__main__":
    start_background()

    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
