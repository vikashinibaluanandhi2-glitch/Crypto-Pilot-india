from flask import Flask, render_template_string, jsonify
import requests
import time

app = Flask(__name__)

cache = {"time": 0, "btc": 0}
CACHE_TIME = 30

def get_btc():
    global cache

    if time.time() - cache["time"] < CACHE_TIME:
        return cache["btc"]

    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=inr"
        data = requests.get(url, timeout=5).json()
        price = data["bitcoin"]["inr"]

        cache["btc"] = price
        cache["time"] = time.time()
        return price

    except:
        return cache["btc"] if cache["btc"] else 0


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Crypto Palette India</title>

<style>
body{
    margin:0;
    font-family:Arial;
    background:black;
    color:white;
    overflow:hidden;
}

/* SPACE BACKGROUND */
.stars, .stars2, .stars3 {
  position:absolute;
  width:100%;
  height:100%;
  display:block;
  background:transparent;
}

.stars {
  background: radial-gradient(white 1px, transparent 1px);
  background-size:50px 50px;
  animation:moveStars 60s linear infinite;
  opacity:0.2;
}

.stars2 {
  background: radial-gradient(#22c55e 1px, transparent 1px);
  background-size:80px 80px;
  animation:moveStars 100s linear infinite;
  opacity:0.2;
}

.stars3 {
  background: radial-gradient(#3b82f6 1px, transparent 1px);
  background-size:120px 120px;
  animation:moveStars 150s linear infinite;
  opacity:0.15;
}

@keyframes moveStars{
  from{transform:translateY(0);}
  to{transform:translateY(-1000px);}
}

/* SIDEBAR */
.sidebar{
    position:fixed;
    width:260px;
    height:100vh;
    background:rgba(15,23,42,0.9);
    padding:20px;
    backdrop-filter:blur(10px);
    border-right:1px solid #1f2937;
}

.logo{
    text-align:center;
    font-size:22px;
    color:#22c55e;
    font-weight:bold;
}

.menu div{
    padding:12px;
    margin:10px 0;
    background:#111827;
    border-radius:10px;
    cursor:pointer;
}

.menu div:hover{
    background:#1f2937;
}

/* MAIN */
.main{
    margin-left:280px;
    padding:20px;
    position:relative;
}

.title{
    font-size:28px;
    font-weight:bold;
}

/* PANELS */
.panel{
    display:none;
    margin-top:20px;
    background:rgba(17,24,39,0.8);
    padding:20px;
    border-radius:15px;
    border:1px solid #1f2937;
}

.active{
    display:block;
}

/* PRICE */
.price{
    font-size:40px;
    color:#22c55e;
    text-shadow:0 0 15px #22c55e;
}

/* FLOATING EFFECT */
.floating-bitcoin{
    position:absolute;
    top:50%;
    left:60%;
    font-size:50px;
    opacity:0.2;
    animation:float 6s ease-in-out infinite;
}

@keyframes float{
    0%{transform:translateY(0);}
    50%{transform:translateY(-30px);}
    100%{transform:translateY(0);}
}
</style>
</head>

<body>

<div class="stars"></div>
<div class="stars2"></div>
<div class="stars3"></div>

<div class="sidebar">
    <div class="logo">Crypto Palette</div>

    <div class="menu">
        <div onclick="openTab('dashboard')">Dashboard</div>
        <div onclick="openTab('markets')">Markets</div>
        <div onclick="openTab('portfolio')">Portfolio</div>
        <div onclick="openTab('wallet')">Wallet</div>
        <div onclick="openTab('settings')">Settings</div>
    </div>
</div>

<div class="main">

    <div class="title">Horizon Crypto Dashboard (INR)</div>

    <div id="dashboard" class="panel active">
        <h2>Bitcoin Live Price</h2>
        <div class="price" id="btc">Loading...</div>
    </div>

    <div id="markets" class="panel">
        <h2>Markets</h2>
        <p>Bitcoin: ₹ <span id="btc2"></span></p>
    </div>

    <div id="portfolio" class="panel">
        <h2>Portfolio</h2>
        <p>Your crypto assets will appear here.</p>
    </div>

    <div id="wallet" class="panel">
        <h2>Wallet</h2>
        <p>Wallet balance system coming soon.</p>
    </div>

    <div id="settings" class="panel">
        <h2>Settings</h2>
        <p>Theme & preferences.</p>
    </div>

</div>

<div class="floating-bitcoin">₿</div>

<script>

/* TAB SYSTEM */
function openTab(tab){
    let panels = document.querySelectorAll(".panel");
    panels.forEach(p => p.classList.remove("active"));
    document.getElementById(tab).classList.add("active");
}

/* LIVE PRICE UPDATE */
async function update(){
    try{
        let res = await fetch("/price");
        let data = await res.json();

        document.getElementById("btc").innerText =
            "₹ " + data.btc.toLocaleString();

        document.getElementById("btc2").innerText =
            data.btc.toLocaleString();

    } catch(e){}
}

/* AUTO UPDATE */
update();
setInterval(update, 5000);

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/price")
def price():
    return jsonify({"btc": get_btc()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
