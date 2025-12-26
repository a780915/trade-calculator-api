async function calculate() {
  const res = await fetch("https://trade-calculator-o6ls.onrender.com/calculate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      direction: "Buy Stop",
      capital: 50000,
      risk_pct: 1,
      entry: 4347.28,
      stop: 4333.5
    })
  });

  const data = await res.json();

  document.getElementById("result").textContent =
`方向：${data.direction}
進場：${data.entry}
止損：${data.stop}
止盈：${data.take_profit}
虧損：${data.actual_loss}
獲利：${data.actual_profit}`;
}
