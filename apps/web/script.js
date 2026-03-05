const DEFAULT_API_BASE = "http://127.0.0.1:8000/v1";
const FALLBACK_SCENARIOS = [
  { id: "phishing-invoice", title: "Phishing Invoice Attack", description: "Credential phishing after invoice link click.", expected_incident_type: "phishing" },
  { id: "account-takeover", title: "Account Takeover", description: "Impossible travel and suspicious MFA prompts.", expected_incident_type: "account_compromise" },
  { id: "endpoint-malware", title: "Endpoint Malware", description: "EDR malware alert and file encryption behavior.", expected_incident_type: "malware" },
];

let apiBase = DEFAULT_API_BASE;
let apiConnected = false;

function requireEl(id) {
  const el = document.getElementById(id);
  if (!el) {
    throw new Error(`Missing required element: #${id}`);
  }
  return el;
}

let result;
let missionResult;
let apiStatus;
let scenarioSelect;
let scenarioCards;
let verboseToggle;
let alarmSummary;
let alarmList;
let apiUrlInput;
let connectBtn;
let scenarioHint;

function setStatus(text, mode) {
  apiStatus.textContent = text;
  apiStatus.classList.remove("ok", "err");
  if (mode) apiStatus.classList.add(mode);
}

function setScenarioHint(text, mode = "warning") {
  scenarioHint.innerHTML = text;
  scenarioHint.classList.remove("warning", "ok");
  scenarioHint.classList.add(mode === "ok" ? "ok" : "warning");
}

function setJsonOrSummary(target, data, summaryLines) {
  if (verboseToggle.checked) {
    target.textContent = JSON.stringify(data, null, 2);
  } else {
    target.textContent = summaryLines.join("\n");
  }
}

function renderScenarioCards(scenarios) {
  scenarioCards.innerHTML = "";
  scenarios.forEach((s) => {
    const card = document.createElement("div");
    card.className = "scenario-card";
    card.innerHTML = `<h3>${s.title}</h3><p>${s.description}</p><code>${s.expected_incident_type}</code>`;
    scenarioCards.appendChild(card);
  });
}

function populateScenarioSelect(scenarios) {
  scenarioSelect.innerHTML = "";
  scenarios.forEach((scenario) => {
    const option = document.createElement("option");
    option.value = scenario.id;
    option.textContent = scenario.title;
    scenarioSelect.appendChild(option);
  });
}

function renderAlarms(alarms) {
  alarmList.innerHTML = "";
  if (!alarms.length) {
    alarmSummary.textContent = "No alarms detected.";
    return;
  }

  const critical = alarms.filter((a) => a.level === "critical").length;
  const warning = alarms.filter((a) => a.level === "warning").length;
  const info = alarms.filter((a) => a.level === "info").length;
  alarmSummary.textContent = `Critical: ${critical} | Warning: ${warning} | Info: ${info}`;

  alarms.forEach((alarm) => {
    const item = document.createElement("div");
    item.className = `alarm-item ${alarm.level}`;
    item.innerHTML = `<strong>${alarm.level.toUpperCase()}</strong> [${alarm.category}] ${alarm.message}`;
    alarmList.appendChild(item);
  });
}

function buildMissionAlarms(data) {
  const alarms = [];
  const report = data.mission_report || {};

  if (!report.triage_match_expected) {
    alarms.push({ level: "critical", category: "classification", message: "Triage did not match expected scenario type." });
  }
  if (data.severity === "critical") {
    alarms.push({ level: "critical", category: "incident", message: "Critical incident requires immediate analyst attention." });
  } else if (data.severity === "high") {
    alarms.push({ level: "warning", category: "incident", message: "High severity incident requires fast containment." });
  }
  if ((report.residual_risk_if_last_action_dropped || 0) >= 0.5) {
    alarms.push({ level: "warning", category: "counterfactual", message: `Residual risk is high (${report.residual_risk_if_last_action_dropped}) if a key action is dropped.` });
  }
  if (report.adversarial_prompt_blocked) {
    alarms.push({ level: "info", category: "safety", message: "Adversarial bypass attempt was blocked by policy checks." });
  }
  return alarms;
}

async function fetchJson(url, options = {}) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 3000);
  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    const payload = await res.json().catch(() => ({}));
    return { ok: res.ok, status: res.status, payload };
  } catch (error) {
    return { ok: false, status: 0, payload: { detail: error.message } };
  } finally {
    clearTimeout(timeoutId);
  }
}

async function connectApi() {
  const chosen = (apiUrlInput.value || DEFAULT_API_BASE).trim();
  apiBase = chosen.replace(/\/$/, "");
  connectBtn.disabled = true;
  connectBtn.textContent = "Connecting...";

  setStatus(`Checking API at ${apiBase} ...`);
  const health = await fetchJson(`${apiBase}/health`);

  if (!health.ok) {
    apiConnected = false;
    setStatus(`API offline (${health.payload.detail || "no response"})`, "err");
    populateScenarioSelect(FALLBACK_SCENARIOS);
    renderScenarioCards(FALLBACK_SCENARIOS);
    setScenarioHint("Could not reach API. Check backend terminal and API URL, then click <strong>Connect API</strong> again.", "warning");
    missionResult.textContent = "API is offline. Start backend and click Connect API again.";
    connectBtn.disabled = false;
    connectBtn.textContent = "Connect API";
    return;
  }

  apiConnected = true;
  setStatus(`API online (${apiBase})`, "ok");

  const scenarios = await fetchJson(`${apiBase}/demo/scenarios`);
  if (!scenarios.ok || !Array.isArray(scenarios.payload) || scenarios.payload.length === 0) {
    populateScenarioSelect(FALLBACK_SCENARIOS);
    renderScenarioCards(FALLBACK_SCENARIOS);
    setScenarioHint("Connected, but <code>/demo/scenarios</code> failed. Showing fallback scenarios.", "warning");
    missionResult.textContent = "Connected, but scenarios endpoint failed. Using fallback scenarios.";
    connectBtn.disabled = false;
    connectBtn.textContent = "Connect API";
    return;
  }

  populateScenarioSelect(scenarios.payload);
  renderScenarioCards(scenarios.payload);
  setScenarioHint("Scenario list loaded. Choose one and click <strong>Run End-to-End Mission</strong>.", "ok");
  missionResult.textContent = "Connected. Select a scenario and click Run End-to-End Mission.";
  connectBtn.disabled = false;
  connectBtn.textContent = "Connect API";
}

async function runScenario() {
  const scenarioId = scenarioSelect.value;
  if (!scenarioId) {
    missionResult.textContent = "Select a scenario first.";
    setScenarioHint("Scenario is empty. Reconnect API and retry.", "warning");
    return;
  }
  if (!apiConnected) {
    missionResult.textContent = "API not connected. Click Connect API first.";
    setScenarioHint("API not connected. Click <strong>Connect API</strong>.", "warning");
    return;
  }

  missionResult.textContent = "Running full mission...";
  const res = await fetchJson(`${apiBase}/demo/run/${scenarioId}`, { method: "POST" });

  if (!res.ok) {
    missionResult.textContent = `Mission failed (${res.status}): ${res.payload.detail || "unknown error"}`;
    renderAlarms([{ level: "critical", category: "runtime", message: missionResult.textContent }]);
    return;
  }

  const data = res.payload;
  const summary = [
    `Mission complete: ${data.scenario_id}`,
    `Ticket: #${data.ticket_id} | Status: ${data.status}`,
    `Incident: ${data.incident_type} | Severity: ${data.severity} | Confidence: ${data.confidence}`,
    `Triage matched expected: ${data.mission_report.triage_match_expected}`,
    `Actions executed: ${data.mission_report.executed_actions}`,
    `Evidence completeness: ${data.mission_report.evidence_completeness}`,
    `Residual risk if last action dropped: ${data.mission_report.residual_risk_if_last_action_dropped}`,
  ];
  setJsonOrSummary(missionResult, data, summary);
  renderAlarms(buildMissionAlarms(data));
  setScenarioHint("Mission executed successfully. Review Mission Report and Alarm Center.", "ok");
}

async function runManualIntake() {
  if (!apiConnected) {
    result.textContent = "API not connected. Click Connect API first.";
    return;
  }

  const userId = document.getElementById("userId").value;
  const message = document.getElementById("message").value;
  result.textContent = "Running intake...";

  const res = await fetchJson(`${apiBase}/chat/intake`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, message }),
  });

  if (!res.ok) {
    result.textContent = `Intake failed (${res.status}): ${res.payload.detail || "unknown error"}`;
    renderAlarms([{ level: "critical", category: "runtime", message: result.textContent }]);
    return;
  }

  const data = res.payload;
  const summary = [
    `Intake created ticket #${data.ticket_id}`,
    `Incident: ${data.incident_type} | Severity: ${data.severity} | Confidence: ${data.confidence}`,
    `Requires approval: ${data.requires_approval}`,
  ];
  setJsonOrSummary(result, data, summary);

  const intakeAlarms = [];
  if (data.severity === "critical") intakeAlarms.push({ level: "critical", category: "incident", message: "Critical severity detected." });
  else if (data.severity === "high") intakeAlarms.push({ level: "warning", category: "incident", message: "High severity detected." });
  else intakeAlarms.push({ level: "info", category: "incident", message: "Non-critical incident received." });
  if (data.requires_approval) intakeAlarms.push({ level: "info", category: "governance", message: "High-risk actions require approval." });
  renderAlarms(intakeAlarms);
}

try {
  result = requireEl("result");
  missionResult = requireEl("missionResult");
  apiStatus = requireEl("apiStatus");
  scenarioSelect = requireEl("scenarioSelect");
  scenarioCards = requireEl("scenarioCards");
  verboseToggle = requireEl("verboseToggle");
  alarmSummary = requireEl("alarmSummary");
  alarmList = requireEl("alarmList");
  apiUrlInput = requireEl("apiUrl");
  connectBtn = requireEl("connectApiBtn");
  scenarioHint = requireEl("scenarioHint");

  connectBtn.addEventListener("click", connectApi);
  requireEl("runScenarioBtn").addEventListener("click", runScenario);
  requireEl("submitBtn").addEventListener("click", runManualIntake);

  apiUrlInput.value = DEFAULT_API_BASE;
  populateScenarioSelect(FALLBACK_SCENARIOS);
  renderScenarioCards(FALLBACK_SCENARIOS);
  setStatus("Not connected. Click Connect API.");
  setScenarioHint("Not connected yet. Click <strong>Connect API</strong>.", "warning");
} catch (error) {
  const err = document.createElement("div");
  err.style.cssText = "margin:12px;padding:10px;border:1px solid #efb2ac;background:#fcefed;border-radius:8px;";
  err.textContent = `UI init failed: ${error.message}. Hard refresh the page.`;
  document.body.prepend(err);
}
