from flask import Flask, render_template_string, jsonify
import requests
import time

app = Flask(__name__)

# cache system (prevents API spam)
cache = {"time": 0, "btc": 0}
CACHE_SECONDS = 30


def get_btc_inr():
    global cache

    if time.time() - cache["time"] < CACHE_SECONDS:
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
    background:#0b1220;
    color:white;
    display:flex;
}

/* SIDEBAR (Horizon VIP style feel) */
.sidebar{
    width:260px;
    height:100vh;
    background:#0f172a;
    padding:20px;
    position:fixed;
    border-right:1px solid #1f2937;
}

.logo{
    font-size:22px;
    font-weight:bold;
    color:#22c55e;
    text-align:center;
    margin-bottom:30px;
}

.menu div{
    padding:12px;
    margin:10px 0;
    background:#111827;
    border-radius:10px;
    cursor:pointer;
    transition:0.2s;
}

.menu div:hover{
    background:#1f2937;
}

/* MAIN AREA */
.main{
    margin-left:280px;
    padding:20px;
    width:100%;
}

.title{
    font-size:28px;
    font-weight:bold;
    margin-bottom:20px;
}

/* DASH CARDS */
.cards{
    display:flex;
    gap:20px;
}

.card{
    background:#111827;
    padding:25px;
    border-radius:15px;
    width:320px;
    box-shadow:0 0 15px rgba(0,0,0,0.5);
    border:1px solid #1f2937;
}

.price{
    font-size:34px;
    color:#22c55e;
    margin-top:10px;
}

.sub{
    color:#9ca3af;
    font-size:13px;
}

.status{
    margin-top:15px;
    font-size:12px;
    color:#9ca3af;
}

/* glow effect like trading apps */
.glow{
    text-shadow:0 0 10px #22c55e;
}
</style>
</head>

<body>

<div class="sidebar">
    <div class="logo">Crypto Palette</div>
    <div class="menu">
        <div>Dashboard</div>
        <div>Markets</div>
        <div>Portfolio</div>
        <div>Wallet</div>
        <div>Settings</div>
    </div>
</div>

<div class="main">

    <div class="title">Horizon-style Crypto Dashboard (INR)</div>

    <div class="cards">

        <div class="card">
            <div class="sub">Bitcoin (BTC)</div>
            <div class="price glow" id="btc">Loading...</div>
            <div class="sub">Live price in Indian Rupees</div>
        </div>

    </div>

    <div class="status" id="status"></div>

</div>

<script>

async function update(){
    try{
        let res = await fetch("/price");
        let data = await res.json();

        document.getElementById("btc").innerText =
            "₹ " + data.btc.toLocaleString();

        document.getElementById("status").innerText =
            "Last updated: " + new Date().toLocaleTimeString();

    }catch(e){
        document.getElementById("status").innerText =
            "Connecting to market data...";
    }
}

// auto update system (NO manual refresh ever)
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
    return jsonify({
        "btc": get_btc_inr()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
