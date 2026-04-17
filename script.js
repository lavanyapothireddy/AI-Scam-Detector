
const API = "http://127.0.0.1:8000/predict";
const ANALYTICS = "http://127.0.0.1:8000/analytics";

function showTab(id) {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

// DETECT
async function predict() {
    let text = document.getElementById("inputText").value;

    let res = await fetch(API, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text})
    });

    let data = await res.json();

    document.getElementById("result").innerHTML =
        `<h2>${data.label}</h2>
         <p>Confidence: ${data.confidence}%</p>`;

    let bar = document.getElementById("barFill");
    bar.style.width = data.confidence + "%";

    loadAnalytics();
}

// DASHBOARD + CHART
async function loadAnalytics() {
    let res = await fetch(ANALYTICS);
    let data = await res.json();

    const ctx = document.getElementById('chart');

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Scam', 'Safe', 'Suspicious'],
            datasets: [{
                data: [data.scam, data.safe, data.suspicious],
                backgroundColor: ['red', 'green', 'yellow']
            }]
        }
    });

    let logDiv = document.getElementById("logList");
    logDiv.innerHTML = "";

    data.history.slice().reverse().forEach(item => {
        let div = document.createElement("div");
        div.innerText = `${item.text} → ${item.label} (${item.confidence}%)`;
        logDiv.appendChild(div);
    });
}

loadAnalytics();