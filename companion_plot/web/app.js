"use strict";

const state = {
  lang: "en", boot: null, cells: [], month: 4, tool: "tomato", picked: null,
  result: null, seq: 0,
};

const $ = (id) => document.getElementById(id);

function detectLang() {
  const saved = localStorage.getItem("companion-plot-lang");
  if (saved === "tr" || saved === "en") return saved;
  return (navigator.language || "en").toLowerCase().startsWith("tr") ? "tr" : "en";
}

function tr(key, values) {
  const table = state.boot.strings[state.lang];
  let text = table[key] ?? state.boot.strings.en[key] ?? key;
  for (const [k, v] of Object.entries(values || {})) text = text.replaceAll(`{${k}}`, v);
  return text;
}

const cropName = (id) => tr(`crop.${id}`);
const emoji = (id) => state.boot.crops[id].emoji;

async function api(path, body) {
  try {
    const res = await fetch(path, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "error.bad_request");
    return data;
  } catch (err) {
    const key = String(err.message).startsWith("error.") ? err.message : "error.network";
    $("suggestion").textContent = tr(key);
    return null;
  }
}

function save() {
  localStorage.setItem("companion-plot-bed", JSON.stringify({ cells: state.cells, month: state.month }));
}

function loadSaved() {
  try {
    const saved = JSON.parse(localStorage.getItem("companion-plot-bed"));
    const size = state.boot.rows * state.boot.cols;
    if (saved && Array.isArray(saved.cells) && saved.cells.length === size) {
      return { cells: saved.cells.map((c) => (c && state.boot.crops[c] ? c : null)), month: saved.month };
    }
  } catch (e) { /* fall through to the sample bed */ }
  return { cells: [...state.boot.sample.cells], month: state.boot.sample.month };
}

function applyStaticText() {
  document.documentElement.lang = state.lang;
  document.title = tr("ui.title");
  document.querySelectorAll("[data-i18n]").forEach((el) => { el.textContent = tr(el.dataset.i18n); });
  document.querySelectorAll(".lang button").forEach((b) => b.classList.toggle("on", b.dataset.lang === state.lang));
  const select = $("month");
  select.innerHTML = "";
  for (let m = 1; m <= 12; m++) {
    const opt = new Option(tr(`month.${m}`), m);
    opt.selected = m === state.month;
    select.add(opt);
  }
}

function renderPalette() {
  const box = $("palette");
  box.innerHTML = "";
  const tools = [...Object.keys(state.boot.crops), ""];
  for (const id of tools) {
    const b = document.createElement("button");
    b.className = "tool" + (state.tool === id ? " on" : "");
    b.innerHTML = `<span class="e">${id ? emoji(id) : "🧽"}</span><span>${id ? cropName(id) : tr("ui.eraser")}</span>`;
    b.onclick = () => { state.tool = id; renderPalette(); renderInfo(); };
    box.append(b);
  }
}

function renderBed() {
  const bed = $("bed");
  bed.innerHTML = "";
  const r = state.result;
  state.cells.forEach((crop, i) => {
    const b = document.createElement("button");
    const mood = r ? r.mood[i] : 0;
    let cls = "cell";
    if (crop && mood > 0) cls += " happy";
    if (crop && mood < 0) cls += " sad";
    if (r && r.off_season.includes(i)) cls += " cold";
    if (state.picked === i) cls += " picked";
    b.className = cls;
    b.setAttribute("aria-label", crop ? cropName(crop) : "-");
    b.textContent = crop ? emoji(crop) : "";
    if (crop && mood !== 0) b.insertAdjacentHTML("beforeend", `<span class="mood">${mood > 0 ? "+" : ""}${mood}</span>`);
    if (r && r.off_season.includes(i)) b.insertAdjacentHTML("beforeend", '<span class="badge">❄️</span>');
    b.onclick = () => plant(i);
    bed.append(b);
  });
}

function pairItem(p, cls) {
  const a = state.cells[p.a], b = state.cells[p.b];
  const text = tr("ui.pair_line", { a: `${emoji(a)} ${cropName(a)}`, b: `${emoji(b)} ${cropName(b)}` });
  return `<li>${text}<span class="fx ${cls}">${p.effect > 0 ? "+" : ""}${p.effect}</span></li>`;
}

function renderScore() {
  const r = state.result;
  if (!r) return;
  $("percent").textContent = r.percent;
  $("meter-fill").style.width = `${r.percent}%`;
  $("planted").textContent = tr("ui.planted", { n: r.planted });
  $("verdict").textContent = tr(`verdict.${r.verdict}`);
  const good = r.pairs.filter((p) => p.effect > 0).sort((x, y) => y.effect - x.effect).slice(0, 4);
  const bad = r.pairs.filter((p) => p.effect < 0).sort((x, y) => x.effect - y.effect).slice(0, 4);
  const none = `<li class="none">${tr("ui.none_yet")}</li>`;
  $("pairs-good").innerHTML = good.length ? good.map((p) => pairItem(p, "up")).join("") : none;
  $("pairs-bad").innerHTML = bad.length ? bad.map((p) => pairItem(p, "down")).join("") : none;
}

function renderInfo() {
  const box = $("crop-info");
  const id = state.tool;
  if (!id) { box.hidden = true; return; }
  box.hidden = false;
  const c = state.boot.crops[id];
  const list = (ids, cls) => `<div class="info-list ${cls}">${ids.map((x) => `<span>${emoji(x)} ${cropName(x)}</span>`).join("")}</div>`;
  const months = c.sow.map((m) => tr(`month.${m}`)).join(", ");
  box.innerHTML = `<h2>${emoji(id)} ${tr("ui.friends_of", { crop: cropName(id) })}</h2>${list(c.friends, "good")}` +
    `<h2>${tr("ui.foes_of")}</h2>${list(c.foes, "bad")}<h2>${tr("ui.sow_window")}</h2><div>${months}</div>`;
}

function renderCalendar() {
  const box = $("calendar");
  const crops = [...new Set(state.cells.filter(Boolean))].sort();
  let html = '<div class="cal-row cal-head"><div></div>';
  for (let m = 1; m <= 12; m++) html += `<div class="cal-cell">${tr(`month.${m}`).slice(0, 3)}</div>`;
  html += "</div>";
  for (const id of crops) {
    html += `<div class="cal-row"><div>${emoji(id)}</div>`;
    const harvest = state.result ? state.result.harvest[id] : null;
    for (let m = 1; m <= 12; m++) {
      const sow = state.boot.crops[id].sow.includes(m);
      const cls = "cal-cell" + (sow ? " sow" : "") + (m === state.month ? " now" : "");
      html += `<div class="${cls}">${m === harvest ? "🧺" : ""}</div>`;
    }
    html += "</div>";
  }
  box.innerHTML = html;
}

function renderAll() {
  renderBed(); renderScore(); renderInfo(); renderCalendar();
}

async function refresh() {
  const ticket = ++state.seq;
  const result = await api("/api/analyze", { cells: state.cells, month: state.month });
  if (!result || ticket !== state.seq) return;
  state.result = result;
  renderAll();
}

function plant(i) {
  state.picked = i;
  const next = state.tool || null;
  state.cells[i] = state.cells[i] === next ? null : next;
  $("suggestion").textContent = "";
  save();
  renderBed();
  refresh();
}

async function suggest() {
  const box = $("suggestion");
  if (state.picked === null) { box.textContent = tr("ui.suggest_pick"); return; }
  const res = await api("/api/suggest", { cells: state.cells, month: state.month, index: state.picked });
  if (!res) return;
  const current = state.cells[state.picked];
  if (res.crop === current) box.textContent = tr("ui.suggest_best");
  else if (current === null && res.gain <= 0) box.textContent = tr("ui.suggest_fill", { crop: cropName(res.crop) });
  else box.textContent = tr("ui.suggest_here", { crop: `${emoji(res.crop)} ${cropName(res.crop)}`, gain: res.gain });
}

function setLang(lang) {
  state.lang = lang;
  localStorage.setItem("companion-plot-lang", lang);
  $("suggestion").textContent = "";
  applyStaticText();
  renderPalette();
  renderAll();
}

async function start() {
  state.boot = await (await fetch("/api/bootstrap")).json();
  state.lang = detectLang();
  Object.assign(state, loadSaved());
  document.querySelectorAll(".lang button").forEach((b) => { b.onclick = () => setLang(b.dataset.lang); });
  $("month").onchange = (e) => { state.month = Number(e.target.value); save(); refresh(); };
  $("btn-help").onclick = suggest;
  $("btn-sample").onclick = () => {
    state.cells = [...state.boot.sample.cells]; state.month = state.boot.sample.month;
    state.picked = null; applyStaticText(); save(); refresh();
  };
  $("btn-clear").onclick = () => {
    state.cells = state.cells.map(() => null); state.picked = null; save(); refresh();
  };
  applyStaticText();
  renderPalette();
  await refresh();
}

start();
