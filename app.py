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

/* SPACE BACKGROUND */
.bg{
    position:fixed;
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
.p2{width:120px;height:120px;background:radial-gradient(circle,#3b82f6,#1e3a8a);top:60%;left:10%;}
.p3{width:70px;height:70px;background:radial-gradient(circle,#f59e0b,#7c2d12);top:40%;left:40%;}

@keyframes float{
    0%{transform:translateY(0);}
    50%{transform:translateY(-25px);}
    100%{transform:translateY(0);}
}

/* SIDEBAR */
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

/* MAIN */
.main{
    margin-left:280px;
    padding:20px;
}

/* PRICE */
.price{
    font-size:50px;
    color:#22c55e;
    text-shadow:0 0 15px #22c55e;
}

/* PINTEREST STYLE GRID */
.grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
    gap:15px;
    margin-top:20px;
}

.card{
    background:#111827;
    padding:15px;
    border-radius:12px;
}

h3{
    color:#22c55e;
}

.small{
    color:#cbd5e1;
    font-size:14px;
    line-height:1.6;
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

<h2>Welcome {{user}}</h2>

<h2>Bitcoin Live Price (INR)</h2>
<div class="price" id="btc">₹ {{initial_price}}</div>

<!-- 🧠 PINTEREST STYLE INFO GRID -->
<div class="grid">

<div class="card">
<h3>What is Bitcoin?</h3>
<div class="small">
Bitcoin is the world’s first decentralized digital currency created in 2009 by Satoshi Nakamoto. 
It is not controlled by any government or bank. Instead, it runs on a global system called blockchain, 
which records every transaction transparently and securely. Bitcoin is often called “digital gold” 
because it is limited in supply and highly valuable in the long term.
</div>
</div>

<div class="card">
<h3>Why Bitcoin price changes?</h3>
<div class="small">
Bitcoin value changes every second because it is driven by global demand and supply. 
When more people buy Bitcoin, the price increases. When people sell, the price drops. 
It is also influenced by news, government regulations, institutional investments, and global economic trends.
</div>
</div>

<div class="card">
<h3>Why INR (Indian Rupees)?</h3>
<div class="small">
This platform shows Bitcoin in Indian Rupees (INR) so users in India can easily understand real value 
without converting USD manually. Since India has a large crypto user base, INR pricing helps traders 
make faster decisions and track profits in their local currency.
</div>
</div>

<div class="card">
<h3>Blockchain Technology</h3>
<div class="small">
Blockchain is a digital ledger system where all Bitcoin transactions are stored in blocks. 
Each block is connected to the previous one, making it impossible to alter history. 
This ensures high security, transparency, and trust without needing any middle authority.
</div>
</div>

<div class="card">
<h3>Fun Facts</h3>
<div class="small">
✔ Only 21 million Bitcoins will ever exist  
✔ First real Bitcoin purchase was 2 pizzas 🍕  
✔ Bitcoin works 24/7 without holidays  
✔ It is used globally like digital money  
</div>
</div>

<div class="card">
<h3>Market Behavior</h3>
<div class="small">
Crypto markets never close. Unlike stock markets, Bitcoin trades 24/7 across the world. 
This makes it highly volatile but also full of opportunities for traders and investors.
</div>
</div>

</div>

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
