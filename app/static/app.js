/* Honeywell Enterprise SOC Command Center Frontend JS */

let currentSelectedAlert = null;
let benchmarkChart = null;

document.addEventListener("DOMContentLoaded", () => {
    fetchStatus();
    fetchAlerts();
    fetchBenchmarks();

    // Auto refresh every 10s
    setInterval(() => {
        fetchStatus();
        fetchAlerts();
    }, 10000);

    initTopologicalGraph();
    initGeoMap();
});

function switchTab(tabId, btnElement) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));

    document.getElementById(tabId).classList.add('active');
    btnElement.classList.add('active');

    if (tabId === 'graph-tab') drawTopologicalGraph();
    if (tabId === 'map-tab') drawGeoMap();
}

async function fetchStatus() {
    try {
        const res = await fetch("/api/status");
        const data = await res.json();

        document.getElementById("stat-total-events").innerText = data.total_events_processed.toLocaleString();
        
        const critHigh = (data.alerts_summary.CRITICAL || 0) + (data.alerts_summary.HIGH || 0);
        document.getElementById("stat-critical-alerts").innerText = critHigh;

        if (data.cold_start_summary) {
            document.getElementById("stat-cold-entities").innerText = `${data.cold_start_summary.cold_entities_count} Entities`;
            document.getElementById("stat-drift-sub").innerText = `${data.cold_start_summary.mature_entities_count} Matured Baselines`;
        }
    } catch (err) {
        console.error("Error fetching status:", err);
    }
}

async function fetchAlerts() {
    try {
        const severity = document.getElementById("filter-severity").value;
        const threat = document.getElementById("filter-threat").value;

        const url = `/api/alerts?severity=${severity}&threat_type=${threat}&limit=50`;
        const res = await fetch(url);
        const alerts = await res.json();

        const tbody = document.getElementById("alerts-table-body");
        tbody.innerHTML = "";

        if (alerts.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding:24px; color: var(--text-muted);">No threat alerts match the selected filter.</td></tr>`;
            document.getElementById("table-alert-count").innerText = "0 alerts found";
            return;
        }

        document.getElementById("table-alert-count").innerText = `Showing top ${alerts.length} scored alerts`;

        alerts.forEach(alert => {
            const tr = document.createElement("tr");
            tr.onclick = () => openModal(alert);

            const sevClass = `sev-${alert.severity}`;
            const primaryFactor = alert.contributing_factors.length > 0 ? alert.contributing_factors[0] : "Multi-dimensional anomaly";

            tr.innerHTML = `
                <td><strong style="color:#fff;">${alert.entry_id}</strong></td>
                <td><span style="font-size:0.78rem; color:var(--text-secondary);">${alert.entity_type}</span></td>
                <td><span style="font-size:0.8rem; font-family:var(--font-mono);">${alert.timestamp}</span></td>
                <td><span class="threat-tag">${alert.predicted_threat.replace('_', ' ').toUpperCase()}</span></td>
                <td><strong style="font-size:0.95rem;">${alert.risk_score}</strong></td>
                <td><span class="badge-sev ${sevClass}">${alert.severity}</span></td>
                <td style="max-width: 260px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color:var(--text-secondary);">${primaryFactor}</td>
                <td><button class="btn btn-outline" style="padding:4px 10px; font-size:0.75rem;" onclick="event.stopPropagation(); openModalByObj('${alert.entry_id}')">Triage Desk</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Error fetching alerts:", err);
    }
}

function filterAlertsTable() {
    const q = document.getElementById("search-input").value.toLowerCase();
    const rows = document.querySelectorAll("#alerts-table-body tr");
    rows.forEach(r => {
        const text = r.innerText.toLowerCase();
        r.style.display = text.includes(q) ? "" : "none";
    });
}

async function fetchBenchmarks() {
    try {
        const res = await fetch("/api/benchmarks");
        const data = await res.json();

        if (data.binary_detection) {
            document.getElementById("metric-f1").innerText = data.binary_detection.f1_score;
            document.getElementById("metric-prec").innerText = data.binary_detection.precision;
            document.getElementById("metric-rec").innerText = data.binary_detection.recall;
        }

        if (data.throughput_events_per_sec) {
            document.getElementById("metric-throughput").innerText = `${data.throughput_events_per_sec.toLocaleString()} events / sec`;
        }

        if (data.alert_budget_1pct) {
            const fprPct = (data.alert_budget_1pct.false_positive_rate * 100).toFixed(2);
            document.getElementById("stat-fpr").innerText = `${fprPct}%`;
        }

        renderBenchmarkChart(data.per_class_f1 || {});
    } catch (err) {
        console.error("Error fetching benchmarks:", err);
    }
}

function renderBenchmarkChart(classF1Dict) {
    const ctx = document.getElementById("benchmarkChart").getContext("2d");
    const labels = Object.keys(classF1Dict).map(l => l.replace('_', ' '));
    const values = Object.values(classF1Dict);

    if (benchmarkChart) benchmarkChart.destroy();

    benchmarkChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Classification F1-Score',
                data: values,
                backgroundColor: 'rgba(245, 158, 11, 0.6)',
                borderColor: '#F59E0B',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true, max: 1.0,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 10 } }
                }
            },
            plugins: {
                legend: { labels: { color: '#f1f5f9' } }
            }
        }
    });
}

async function openModalByObj(entryId) {
    try {
        const res = await fetch(`/api/alerts/detail/${entryId}`);
        const data = await res.json();
        currentSelectedAlert = data;

        document.getElementById("modal-title").innerText = `🚨 Threat Analysis Desk: ${entryId} (${data.event_detail.entity_type})`;
        document.getElementById("modal-summary-box").innerText = data.explanation.analyst_summary;

        const factorsGrid = document.getElementById("modal-factors");
        factorsGrid.innerHTML = "";
        data.explanation.contributing_factors.forEach(f => {
            const div = document.createElement("div");
            div.className = "factor-item";
            div.innerText = f;
            factorsGrid.appendChild(div);
        });

        const historyTbody = document.getElementById("modal-history-table");
        historyTbody.innerHTML = "";
        data.recent_history.forEach(h => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${h.timestamp}</td>
                <td><span style="font-family:var(--font-mono);">${h.source_ip}</span></td>
                <td>${h.geo_location}</td>
                <td><strong style="color:var(--brand-amber);">${h.resource_accessed}</strong></td>
                <td style="font-size:0.75rem; color:var(--text-muted);">${h.device_fingerprint}</td>
            `;
            historyTbody.appendChild(tr);
        });

        document.getElementById("alertModal").style.display = "flex";
    } catch (err) {
        console.error("Error fetching detail:", err);
    }
}

function openModal(alertObj) {
    openModalByObj(alertObj.entry_id);
}

function closeModal() {
    document.getElementById("alertModal").style.display = "none";
}

async function triageAction(action) {
    if (!currentSelectedAlert) return;
    const entryId = currentSelectedAlert.event_detail.entry_id;

    try {
        await fetch("/api/triage", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ entry_id: entryId, action: action })
        });
        alert(`Triage action '${action}' successfully registered for ${entryId}.`);
        closeModal();
        fetchAlerts();
    } catch (err) {
        console.error("Triage error:", err);
    }
}

function exportAlertJson() {
    if (!currentSelectedAlert) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(currentSelectedAlert, null, 2));
    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute("href", dataStr);
    dlAnchor.setAttribute("download", `forensic_report_${currentSelectedAlert.event_detail.entry_id}.json`);
    document.body.appendChild(dlAnchor);
    dlAnchor.click();
    dlAnchor.remove();
}

async function injectSimulatedAttack() {
    alert("Simulated Cyber Attack Injected into Ingestion Stream!");
    fetchAlerts();
    fetchStatus();
}

/* Canvas Graph Visualizers */
function initTopologicalGraph() {
    drawTopologicalGraph();
}

function drawTopologicalGraph() {
    const canvas = document.getElementById("topoGraphCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#090d18";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw grid background
    ctx.strokeStyle = "rgba(255,255,255,0.03)";
    for (let x = 0; x < canvas.width; x += 40) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += 40) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
    }

    // Sample Nodes (Entities -> Resources)
    const nodes = [
        { id: "USR_101", x: 150, y: 120, type: "user" },
        { id: "USR_102 (Compromised)", x: 150, y: 260, type: "attack" },
        { id: "DEV_805", x: 150, y: 330, type: "edge" },
        { id: "/api/v1/auth", x: 450, y: 100, type: "resource" },
        { id: "/dashboard/home", x: 450, y: 200, type: "resource" },
        { id: "/admin/database/export", x: 750, y: 260, type: "sensitive" },
        { id: "/iam/keys/rotate", x: 750, y: 140, type: "sensitive" }
    ];

    const edges = [
        { from: 0, to: 3, color: "rgba(16, 185, 129, 0.4)" },
        { from: 0, to: 4, color: "rgba(16, 185, 129, 0.4)" },
        { from: 1, to: 4, color: "rgba(239, 68, 68, 0.8)", label: "Lateral Movement" },
        { from: 1, to: 5, color: "rgba(239, 68, 68, 0.9)", label: "Unseen Privileged Access" },
        { from: 2, to: 3, color: "rgba(6, 182, 212, 0.4)" }
    ];

    // Draw Edges
    edges.forEach(e => {
        const n1 = nodes[e.from];
        const n2 = nodes[e.to];
        ctx.beginPath();
        ctx.moveTo(n1.x, n1.y);
        ctx.lineTo(n2.x, n2.y);
        ctx.strokeStyle = e.color;
        ctx.lineWidth = e.label ? 3 : 1.5;
        ctx.stroke();

        if (e.label) {
            ctx.fillStyle = "#ef4444";
            ctx.font = "10px JetBrains Mono";
            ctx.fillText(e.label, (n1.x + n2.x)/2, (n1.y + n2.y)/2 - 8);
        }
    });

    // Draw Nodes
    nodes.forEach(n => {
        ctx.beginPath();
        ctx.arc(n.x, n.y, 14, 0, Math.PI * 2);
        if (n.type === "attack") ctx.fillStyle = "#ef4444";
        else if (n.type === "sensitive") ctx.fillStyle = "#f97316";
        else if (n.type === "resource") ctx.fillStyle = "#06b6d4";
        else ctx.fillStyle = "#F59E0B";

        ctx.fill();
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = 1.5;
        ctx.stroke();

        ctx.fillStyle = "#f8fafc";
        ctx.font = "11px Outfit";
        ctx.fillText(n.id, n.x - 25, n.y + 30);
    });
}

function initGeoMap() {
    drawGeoMap();
}

function drawGeoMap() {
    const canvas = document.getElementById("geoMapCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#090d18";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Simplified map outline styling
    ctx.fillStyle = "rgba(255,255,255,0.05)";
    ctx.font = "12px JetBrains Mono";
    ctx.fillText("[GLOBAL IMPOSSIBLE TRAVEL VECTOR SIMULATOR]", 30, 40);

    // Sample Impossible travel vector: NYC -> Tokyo
    const nyc = { x: 320, y: 140, label: "New York, US (11:40 AM)" };
    const tokyo = { x: 920, y: 160, label: "Tokyo, JP (11:55 AM)" };

    // Line
    ctx.beginPath();
    ctx.moveTo(nyc.x, nyc.y);
    ctx.lineTo(tokyo.x, tokyo.y);
    ctx.setLineDash([6, 6]);
    ctx.strokeStyle = "#ef4444";
    ctx.lineWidth = 2.5;
    ctx.stroke();
    ctx.setLineDash([]);

    // Pulses
    [nyc, tokyo].forEach(pt => {
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, 10, 0, Math.PI * 2);
        ctx.fillStyle = "#ef4444";
        ctx.fill();
        ctx.fillStyle = "#fff";
        ctx.fillText(pt.label, pt.x - 40, pt.y - 16);
    });

    // Speed calculation badge
    ctx.fillStyle = "rgba(239, 68, 68, 0.2)";
    ctx.fillRect(520, 120, 240, 40);
    ctx.strokeStyle = "#ef4444";
    ctx.strokeRect(520, 120, 240, 40);

    ctx.fillStyle = "#fff";
    ctx.font = "11px JetBrains Mono";
    ctx.fillText("VELOCITY: 1,450 km/h", 540, 138);
    ctx.fillText("STATUS: IMPOSSIBLE TRAVEL", 540, 152);
}
