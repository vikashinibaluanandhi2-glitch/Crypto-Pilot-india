from flask import Flask
import urllib.request, json

app = Flask(__name__)

# 🔥 Get Live Crypto Price in INR
def get_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=inr"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data["ethereum"]["inr"]
    except:
        return 200000  # fallback

@app.route("/")
def home():
    eth_price = get_price()

    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>CryptoPilot India</title>

    <style>
        body {{
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0B0F1A, #111827);
            color: white;
        }}

        .header {{
            padding: 20px;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: #6366F1;
        }}

        .container {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            padding: 20px;
        }}

        .card {{
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 15px;
            width: 280px;
            text-align: center;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
        }}

        button {{
            background: #6366F1;
            border: none;
            padding: 10px 20px;
            color: white;
            border-radius: 8px;
            cursor: pointer;
        }}

        button:hover {{
            background: #4f46e5;
        }}

        input {{
            padding: 8px;
            width: 80%;
            margin-top: 10px;
            border-radius: 6px;
            border: none;
        }}
    </style>
</head>

<body>

    <div class="header">CryptoPilot India</div>

    <div style="text-align:center;">
        <button onclick="connectWallet()">Connect Wallet</button>
    </div>

    <div class="container">

        <div class="card">
            <h3>Live ETH Price</h3>
            <p id="livePrice">₹ {eth_price}</p>
        </div>

        <div class="card">
            <h3>Total Balance</h3>
            <p id="balance">₹ 0</p>
        </div>

        <div class="card">
            <h3>Wallet</h3>
            <p id="wallet">Not Connected</p>
        </div>

        <div class="card">
            <h3>Invest / Withdraw</h3>
            <input id="amount" placeholder="Enter ₹">
            <br><br>
            <button onclick="invest()">Invest</button>
            <button onclick="withdraw()">Withdraw</button>
        </div>

        <div class="card">
            <h3>AI Suggestion 🤖</h3>
            <p>Market stable — hold assets</p>
        </div>

    </div>

<script src="https://cdn.jsdelivr.net/npm/ethers/dist/ethers.min.js"></script>

<script>
    let ethPrice = {eth_price};
    let currentBalance = 0;

    async function connectWallet() {{
        if (window.ethereum) {{
            const accounts = await window.ethereum.request({{
                method: 'eth_requestAccounts'
            }});

            document.getElementById("wallet").innerText = accounts[0];

            const provider = new ethers.providers.Web3Provider(window.ethereum);
            const balance = await provider.getBalance(accounts[0]);
            const eth = parseFloat(ethers.utils.formatEther(balance));

            currentBalance = eth * ethPrice;

            document.getElementById("balance").innerText =
                "₹ " + currentBalance.toFixed(2);
        }} else {{
            alert("Install MetaMask");
        }}
    }}

    // 🔄 AUTO UPDATE PRICE
    async function updatePrice() {{
        try {{
            let response = await fetch("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=inr");
            let data = await response.json();

            ethPrice = data.ethereum.inr;

            document.getElementById("livePrice").innerText =
                "₹ " + ethPrice;
        }} catch (e) {{
            console.log("Update failed");
        }}
    }}

    setInterval(updatePrice, 60000);

    function invest() {{
        let amt = parseFloat(document.getElementById("amount").value);

        if (!amt || amt <= 0) {{
            alert("Enter valid amount");
            return;
        }}

        currentBalance += amt;

        document.getElementById("balance").innerText =
            "₹ " + currentBalance.toFixed(2);
    }}

    function withdraw() {{
        let amt = parseFloat(document.getElementById("amount").value);

        if (!amt || amt <= 0) {{
            alert("Enter valid amount");
            return;
        }}

        if (amt > currentBalance) {{
            alert("Not enough balance");
            return;
        }}

        currentBalance -= amt;

        document.getElementById("balance").innerText =
            "₹ " + currentBalance.toFixed(2);
    }}
</script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)