from flask import Flask, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Crypto Palette India</title>

<style>
body{
    margin:0;
    font-family:Arial;
    background:#0a0f1f;
    color:white;
    display:flex;
}

/* SIDEBAR (ORIZON STYLE) */
.sidebar{
    width:220px;
    background:#0f172a;
    height:100vh;
    padding:20px;
    position:fixed;
}

.sidebar h2{
    color:#22c55e;
    text-align:center;
}

.menu{
    margin-top:30px;
}

.menu div{
    padding:12px;
    margin:8px 0;
    background:#111827;
    border-radius:10px;
    cursor:pointer;
}

.menu div:hover{
    background:#1f2937;
}

/* MAIN AREA */
.main{
    margin-left:240px;
    padding:20px;
    width:100%;
}

.header{
    font-size:26px;
    font-weight:bold;
    margin-bottom:20px;
}

/* CARDS */
.cards{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:20px;
}

.card{
    background:#111827;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0 0 10px rgba(0,0,0,0.5);
}

.price{
    font-size:22px;
    color:#22c55e;
    margin-top:10px;
}

.table{
    margin-top:30px;
    background:#111827;
    padding:15px;
    border-radius:15px;
}

.row{
    display:flex;
    justify-content:space-between;
    padding:10px;
    border-bottom:1px solid #1f2937;
}
</style>
</head>

<body>

<div class="sidebar">
    <h2>Crypto Palette</h2>
    <div class="menu">
        <div>Dashboard</div>
        <div>Markets</div>
        <div>Portfolio</div>
        <div>Wallet</div>
    </div>
</div>

<div class="main">

    <div class="header">Crypto Dashboard (INR Live)</div>

    <div class="cards">
        <div class="card">
            <h3>Bitcoin</h3>
            <div class="price" id="btc">Loading...</div>
        </div>

        <div class="card">
            <h3>Ethereum</h3>
            <div class="price" id="eth">Loading...</div>
        </div>

        <div class="card">
            <h3>Dogecoin</h3>
            <div class="price" id="doge">Loading...</div>
        </div>
    </div>

    <div class="table">
        <h3>Market Overview</h3>
        <div class="row"><span>BTC</span><span id="btc2"></span></div>
        <div class="row"><span>ETH</span><span id="eth2"></span></div>
        <div class="row"><span>DOGE</span><span id="doge2"></span></div>
    </div>

</div>

<script>

async function update(){
    let res = await fetch("/prices");
    let data = await res.json();

    document.getElementById("btc").innerText = "₹ " + data.btc;
    document.getElementById("eth").innerText = "₹ " + data.eth;
    document.getElementById("doge").innerText = "₹ " + data.doge;

    document.getElementById("btc2").innerText = "₹ " + data.btc;
    document.getElementById("eth2").innerText = "₹ " + data.eth;
    document.getElementById("doge2").innerText = "₹ " + data.doge;
}

update();
setInterval(update, 4000);

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/prices")
def prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,dogecoin&vs_currencies=inr"
    data = requests.get(url).json()

    return {
        "btc": f"{data['bitcoin']['inr']:,}",
        "eth": f"{data['ethereum']['inr']:,}",
        "doge": f"{data['dogecoin']['inr']:,}"
    }

if __name__ == "__main__":
    app.run(debug=True)
