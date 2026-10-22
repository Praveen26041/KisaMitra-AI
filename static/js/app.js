(() => {
"use strict";

/* ---------- i18n ---------- */
const T = {
  en: {
    tagline: "Weather-aware, budget-aware farming guidance",
    tabWeather: "Weather", tabCrops: "Crop advice", tabSim: "What-if simulator", tabCal: "Farming calendar",
    wTitle: "Local weather forecast", locPh: "Town, city or district", search: "Search",
    forecast7: "7-day forecast", source: "Source",
    cTitle: "Crop recommendation",
    cHelp: "Enter soil-test values and farm details. Seasonal rainfall must be entered by you; the weather tab can fill temperature and humidity.",
    fN: "Nitrogen N (kg/ha)", fP: "Phosphorus P (kg/ha)", fK: "Potassium K (kg/ha)", fPh: "Soil pH",
    fT: "Temperature (°C)", fH: "Humidity (%)", fR: "Seasonal rainfall (mm)", fLand: "Land (acres)",
    fBudget: "Budget (₹)", fIrr: "Irrigation", irrAvail: "Available", irrLimited: "Limited",
    getRec: "Get recommendations", fillWeather: "Fill from loaded weather",
    sTitle: "What-if farming simulator",
    sHelp: "Compare crops side by side and stress-test cost and price assumptions. All figures are illustrative.",
    sCrops: "Crops to compare", sPrice: "Market price change", sCost: "Input cost change",
    sYield: "Yield change (weather loss / gain)",
    notice: "Economics are illustrative planning assumptions, not guaranteed yield, market price, or profit. Confirm locally with a KVK/agriculture officer.",
    calTitle: "Weather-adaptive farming calendar",
    calHelp: "Pick a crop and sowing date. Activities are re-checked against the latest forecast whenever you refresh.",
    calBuild: "Build / refresh plan",
    disclaimer: "Decision-support prototype, not professional agronomic advice. Confirm crop, chemical, irrigation and financial decisions with local agricultural experts.",
    // dynamic
    feels: "Feels like", humidity: "Humidity", wind: "Wind", rain: "Rain", cloud: "Cloud", pressure: "Pressure",
    day: "Date", hi: "Max °C", lo: "Min °C", rainMm: "Rain mm", rainP: "Rain %", windKm: "Wind km/h", uv: "UV", et0: "ET₀ mm",
    tempChart: "Temperature (°C)", rainChart: "Rain (mm)", rainProbChart: "Rain chance (%)",
    loading: "Loading…", enterLoc: "Enter a town, city or district.", loadWeatherFirst: "Load the weather first.",
    filled: "Temperature and humidity filled from the 7-day forecast. Enter seasonal rainfall yourself.",
    modelRF: "Trained ML model active", modelBase: "Baseline demo (model not trained)",
    method: "Method", score: "Match", scoreBase: "Baseline match", cost: "Est. cost", gross: "Est. revenue", net: "Est. net",
    days: "Days", water: "Water need", season: "Season", withinBudget: "Within budget", overBudget: "Over budget",
    why: "Why this suggestion", high: "high", medium: "medium", low: "low",
    crop: "Crop", price: "Price", yield: "Yield (t)", simNet: "Net (₹)",
    simPick: "Select at least one crop.", costAxis: "₹ (estimated)", costLbl: "Cost", grossLbl: "Revenue", netLbl: "Net",
    timeline: "Crop-stage timeline", next7: "Next 7 days: forecast-adjusted actions", calNeedCrop: "Choose a crop first.",
    calNeedWeather: "Load the weather in the Weather tab first, so the plan can use the forecast.",
    calDone: "Plan updated with the latest forecast.",
    maxT: "Max", rainW: "Rain", windW: "Wind", changed: "Plan changed since last refresh",
    errGeneric: "Something went wrong. Please try again.",
    wcode: { 0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast", 45: "Fog", 48: "Fog", 51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
      61: "Light rain", 63: "Rain", 65: "Heavy rain", 80: "Rain showers", 81: "Rain showers", 82: "Violent showers", 95: "Thunderstorm", 96: "Thunderstorm", 99: "Thunderstorm" },
    alert_rain: "High rain chance ({v}%). Review irrigation and avoid spraying before rain.",
    alert_heavy: "Forecast rainfall {v} mm. Check drainage and field access.",
    alert_wind: "Strong wind forecast ({v} km/h). Secure light structures and review spraying.",
    st_go: "Go", st_hold: "Hold", st_skip: "Skip", st_warn: "Watch",
    adv: {
      spray_hold: "Hold pesticide/herbicide spraying – rain likely, product would wash off.",
      fert_hold: "Postpone fertilizer top-dressing – rain can leach nutrients.",
      irrigation_skip: "Skip irrigation – rain is expected.",
      spray_ok: "Good window for spraying (low wind, no major rain).",
      wind_hold: "Hold spraying – wind is too strong, spray will drift.",
      irrigate_high_et: "High evaporation – irrigate early morning or evening.",
      drainage: "Heavy rain – check field drainage and avoid machinery in wet soil.",
      heat: "Very hot day – protect young plants, irrigate in cooler hours.",
      cold: "Cold day – protect seedlings from chill/frost."
    },
    stage: { prep: "Land preparation and basal manure", sowing: "Sowing / transplanting", irrigation: "First irrigation check", weeding: "Weeding",
      fertilizer: "Top-dress fertilizer (split dose)", pest: "Pest and disease scouting", harvest: "Expected harvest window" },
    reasons: {
      "High rainfall input favours crops that can use wetter conditions; verify drainage.": "High rainfall input favours crops that can use wetter conditions; verify drainage.",
      "Lower rainfall input makes water planning especially important.": "Lower rainfall input makes water planning especially important.",
      "Entered soil pH is within a broadly common crop-growing range.": "Entered soil pH is within a broadly common crop-growing range.",
      "Water demand may conflict with your limited irrigation.": "Water demand may conflict with your limited irrigation.",
      "Estimated cultivation cost exceeds the entered budget.": "Estimated cultivation cost exceeds the entered budget.",
      "This crop ranked near the top for the entered soil and climate values.": "This crop ranked near the top for the entered soil and climate values."
    }
  },
  hi: {
    tagline: "मौसम और बजट के अनुसार खेती की सलाह",
    tabWeather: "मौसम", tabCrops: "फसल सलाह", tabSim: "क्या-अगर सिम्युलेटर", tabCal: "खेती कैलेंडर",
    wTitle: "स्थानीय मौसम पूर्वानुमान", locPh: "कस्बा, शहर या ज़िला", search: "खोजें",
    forecast7: "7 दिन का पूर्वानुमान", source: "स्रोत",
    cTitle: "फसल सुझाव",
    cHelp: "मिट्टी जांच के मान और खेत का विवरण भरें। मौसमी वर्षा आपको स्वयं भरनी होगी; मौसम टैब तापमान और आर्द्रता भर सकता है।",
    fN: "नाइट्रोजन N (किग्रा/हे.)", fP: "फॉस्फोरस P (किग्रा/हे.)", fK: "पोटैशियम K (किग्रा/हे.)", fPh: "मिट्टी का pH",
    fT: "तापमान (°C)", fH: "आर्द्रता (%)", fR: "मौसमी वर्षा (मिमी)", fLand: "ज़मीन (एकड़)",
    fBudget: "बजट (₹)", fIrr: "सिंचाई", irrAvail: "उपलब्ध", irrLimited: "सीमित",
    getRec: "सुझाव पाएं", fillWeather: "लोड किए मौसम से भरें",
    sTitle: "क्या-अगर खेती सिम्युलेटर",
    sHelp: "फसलों की तुलना करें और लागत व भाव की मान्यताओं को परखें। सभी आंकड़े केवल अनुमानित हैं।",
    sCrops: "तुलना के लिए फसलें", sPrice: "बाज़ार भाव में बदलाव", sCost: "लागत में बदलाव",
    sYield: "उपज में बदलाव (मौसम से नुकसान/लाभ)",
    notice: "आर्थिक आंकड़े केवल अनुमानित योजना-मान्यताएं हैं, उपज, बाज़ार भाव या मुनाफ़े की गारंटी नहीं। स्थानीय KVK/कृषि अधिकारी से पुष्टि करें।",
    calTitle: "मौसम के अनुसार बदलने वाला खेती कैलेंडर",
    calHelp: "फसल और बुवाई की तारीख चुनें। हर बार रिफ्रेश करने पर गतिविधियां ताज़ा पूर्वानुमान से दोबारा जांची जाती हैं।",
    calBuild: "योजना बनाएं / रिफ्रेश करें",
    disclaimer: "यह निर्णय-सहायता प्रोटोटाइप है, पेशेवर कृषि सलाह नहीं। फसल, रसायन, सिंचाई और वित्तीय निर्णय स्थानीय कृषि विशेषज्ञों से पक्के करें।",
    feels: "महसूस होता है", humidity: "आर्द्रता", wind: "हवा", rain: "वर्षा", cloud: "बादल", pressure: "दबाव",
    day: "तारीख", hi: "अधिकतम °C", lo: "न्यूनतम °C", rainMm: "वर्षा मिमी", rainP: "वर्षा %", windKm: "हवा किमी/घं.", uv: "UV", et0: "ET₀ मिमी",
    tempChart: "तापमान (°C)", rainChart: "वर्षा (मिमी)", rainProbChart: "वर्षा की संभावना (%)",
    loading: "लोड हो रहा है…", enterLoc: "कस्बा, शहर या ज़िला लिखें।", loadWeatherFirst: "पहले मौसम लोड करें।",
    filled: "तापमान और आर्द्रता 7 दिन के पूर्वानुमान से भरे गए। मौसमी वर्षा स्वयं भरें।",
    modelRF: "प्रशिक्षित ML मॉडल सक्रिय", modelBase: "बेसलाइन डेमो (मॉडल प्रशिक्षित नहीं)",
    method: "विधि", score: "मिलान", scoreBase: "बेसलाइन मिलान", cost: "अनुमानित लागत", gross: "अनुमानित आय", net: "अनुमानित शुद्ध",
    days: "दिन", water: "पानी की ज़रूरत", season: "मौसम", withinBudget: "बजट के भीतर", overBudget: "बजट से ऊपर",
    why: "यह सुझाव क्यों", high: "अधिक", medium: "मध्यम", low: "कम",
    crop: "फसल", price: "भाव", yield: "उपज (टन)", simNet: "शुद्ध (₹)",
    simPick: "कम से कम एक फसल चुनें।", costAxis: "₹ (अनुमानित)", costLbl: "लागत", grossLbl: "आय", netLbl: "शुद्ध",
    timeline: "फसल-चरण समयरेखा", next7: "अगले 7 दिन: पूर्वानुमान के अनुसार कार्य", calNeedCrop: "पहले फसल चुनें।",
    calNeedWeather: "पहले मौसम टैब में मौसम लोड करें, ताकि योजना पूर्वानुमान का उपयोग कर सके।",
    calDone: "ताज़ा पूर्वानुमान के साथ योजना अपडेट हुई।",
    maxT: "अधिकतम", rainW: "वर्षा", windW: "हवा", changed: "पिछली बार से योजना बदली",
    errGeneric: "कुछ गड़बड़ हुई। कृपया फिर कोशिश करें।",
    wcode: { 0: "साफ़ आसमान", 1: "ज़्यादातर साफ़", 2: "आंशिक बादल", 3: "घने बादल", 45: "कोहरा", 48: "कोहरा", 51: "हल्की फुहार", 53: "फुहार", 55: "तेज़ फुहार",
      61: "हल्की बारिश", 63: "बारिश", 65: "तेज़ बारिश", 80: "बौछारें", 81: "बौछारें", 82: "तेज़ बौछारें", 95: "आंधी-तूफ़ान", 96: "आंधी-तूफ़ान", 99: "आंधी-तूफ़ान" },
    alert_rain: "बारिश की ऊंची संभावना ({v}%)। सिंचाई की समीक्षा करें और बारिश से पहले छिड़काव न करें।",
    alert_heavy: "{v} मिमी वर्षा का पूर्वानुमान। जल-निकासी और खेत तक पहुंच जांचें।",
    alert_wind: "तेज़ हवा का पूर्वानुमान ({v} किमी/घं.)। हल्के ढांचे सुरक्षित करें और छिड़काव पर पुनर्विचार करें।",
    st_go: "करें", st_hold: "रुकें", st_skip: "छोड़ें", st_warn: "ध्यान दें",
    adv: {
      spray_hold: "कीटनाशक/खरपतवारनाशक छिड़काव रोकें – बारिश संभव है, दवा बह जाएगी।",
      fert_hold: "खाद की टॉप-ड्रेसिंग टालें – बारिश से पोषक तत्व बह सकते हैं।",
      irrigation_skip: "सिंचाई छोड़ें – बारिश अपेक्षित है।",
      spray_ok: "छिड़काव के लिए अच्छा समय (कम हवा, बड़ी बारिश नहीं)।",
      wind_hold: "छिड़काव रोकें – हवा बहुत तेज़ है, दवा उड़ जाएगी।",
      irrigate_high_et: "वाष्पीकरण अधिक है – सुबह जल्दी या शाम को सिंचाई करें।",
      drainage: "भारी बारिश – खेत की जल-निकासी जांचें और गीली मिट्टी में मशीन न चलाएं।",
      heat: "बहुत गर्म दिन – छोटे पौधों को बचाएं, ठंडे समय में सिंचाई करें।",
      cold: "ठंडा दिन – पौध को ठंड/पाले से बचाएं।"
    },
    stage: { prep: "खेत की तैयारी और बेसल खाद", sowing: "बुवाई / रोपाई", irrigation: "पहली सिंचाई जांच", weeding: "निराई-गुड़ाई",
      fertilizer: "टॉप-ड्रेसिंग खाद (किस्तों में)", pest: "कीट और रोग निरीक्षण", harvest: "संभावित कटाई अवधि" },
    reasons: {
      "High rainfall input favours crops that can use wetter conditions; verify drainage.": "अधिक वर्षा वाली स्थितियों में उगने वाली फसलें अनुकूल हैं; जल-निकासी जांचें।",
      "Lower rainfall input makes water planning especially important.": "कम वर्षा के कारण पानी की योजना विशेष रूप से ज़रूरी है।",
      "Entered soil pH is within a broadly common crop-growing range.": "दर्ज मिट्टी का pH फसल उगाने की आम सीमा के भीतर है।",
      "Water demand may conflict with your limited irrigation.": "फसल की पानी की मांग आपकी सीमित सिंचाई से टकरा सकती है।",
      "Estimated cultivation cost exceeds the entered budget.": "अनुमानित खेती लागत दर्ज बजट से अधिक है।",
      "This crop ranked near the top for the entered soil and climate values.": "दर्ज मिट्टी और जलवायु मानों के लिए यह फसल शीर्ष के पास रही।"
    }
  }
};
const CROP_HI = { rice: "धान", maize: "मक्का", chickpea: "चना", kidneybeans: "राजमा", pigeonpeas: "अरहर", mothbeans: "मोठ", mungbean: "मूंग", blackgram: "उड़द", lentil: "मसूर", pomegranate: "अनार", banana: "केला", mango: "आम", grapes: "अंगूर", watermelon: "तरबूज़", muskmelon: "खरबूज़ा", apple: "सेब", orange: "संतरा", papaya: "पपीता", coconut: "नारियल", cotton: "कपास", jute: "जूट", coffee: "कॉफ़ी", wheat: "गेहूँ", mustard: "सरसों", potato: "आलू", onion: "प्याज़", tomato: "टमाटर", soybean: "सोयाबीन", groundnut: "मूंगफली", sorghum: "ज्वार", pearlmillet: "बाजरा", okra: "भिंडी" };
const SEASON_HI = { "Kharif": "खरीफ", "Rabi": "रबी", "Kharif/Rabi": "खरीफ/रबी", "Kharif/Summer": "खरीफ/गर्मी", "Summer": "गर्मी", "Perennial": "बारहमासी", "Varies": "भिन्न" };

let lang = "en";
try { lang = localStorage.getItem("km_lang") || "en"; } catch (e) {}
const t = k => (T[lang][k] ?? T.en[k] ?? k);
const cropName = c => lang === "hi" ? (CROP_HI[c] || c) : c;
const seasonName = s => lang === "hi" ? (SEASON_HI[s] || s) : s;
const inr = n => "₹" + Math.round(n).toLocaleString("en-IN");
const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

/* ---------- state ---------- */
const S = { weather: null, crops: null, recs: null, cal: null, charts: {}, health: null, lastCalSig: null };

async function api(url, opts) {
  const r = await fetch(url, opts);
  let j = {};
  try { j = await r.json(); } catch (e) {}
  if (!r.ok) throw new Error(j.error || t("errGeneric"));
  return j;
}
function setMsg(id, text, kind) { const el = $(id); el.textContent = text || ""; el.className = "msg" + (kind ? " " + kind : ""); }

/* ---------- language ---------- */
function applyLang() {
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach(el => { el.textContent = t(el.dataset.i18n); });
  document.querySelectorAll("[data-i18n-ph]").forEach(el => { el.placeholder = t(el.dataset.i18nPh); });
  $("langBtn").textContent = lang === "en" ? "हिंदी" : "English";
  renderBadge();
  if (S.weather) renderWeather();
  if (S.recs) renderRecs();
  fillCropSelects();
  renderSim();
  if (S.cal) renderCalendar();
}
$("langBtn").addEventListener("click", () => {
  lang = lang === "en" ? "hi" : "en";
  try { localStorage.setItem("km_lang", lang); } catch (e) {}
  applyLang();
});

/* ---------- tabs ---------- */
document.querySelectorAll(".tab").forEach(b => b.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach(x => x.classList.toggle("active", x === b));
  document.querySelectorAll(".panel").forEach(p => p.classList.toggle("active", p.id === "tab-" + b.dataset.tab));
  if (b.dataset.tab === "sim") renderSim();
}));

/* ---------- health badge ---------- */
function renderBadge() {
  const b = $("modelBadge");
  if (!S.health) { b.textContent = "…"; return; }
  b.textContent = S.health.ml_model_ready ? t("modelRF") : t("modelBase");
}
api("/api/health").then(h => { S.health = h; renderBadge(); }).catch(() => {});

/* ---------- weather ---------- */
function mkChart(id, cfg) {
  if (typeof Chart === "undefined") return;
  if (S.charts[id]) S.charts[id].destroy();
  S.charts[id] = new Chart($(id), cfg);
}
const fmt = (v, d = 0) => (v === null || v === undefined || Number.isNaN(v)) ? "–" : Number(v).toFixed(d);

function renderWeather() {
  const w = S.weather, c = w.current || {}, d = w.daily || {};
  $("weatherBody").classList.remove("hidden");
  const loc = w.location;
  $("placeName").textContent = [loc.name, loc.admin1, loc.country].filter(Boolean).join(", ");
  const desc = (T[lang].wcode[c.weather_code]) || c.description || "";
  $("weatherDesc").textContent = desc;
  const stats = [
    [fmt(c.temperature_2m, 1) + "°C", lang === "hi" ? "तापमान" : "Temperature"],
    [fmt(c.apparent_temperature, 1) + "°C", t("feels")],
    [fmt(c.relative_humidity_2m) + "%", t("humidity")],
    [fmt(c.wind_speed_10m, 1) + " km/h", t("wind")],
    [fmt(c.precipitation, 1) + " mm", t("rain")],
    [fmt(c.cloud_cover) + "%", t("cloud")],
    [fmt(c.pressure_msl) + " hPa", t("pressure")],
  ];
  $("currentStats").innerHTML = stats.map(([v, l]) => `<div class="stat"><b>${esc(v)}</b><span>${esc(l)}</span></div>`).join("");

  // alerts (translated from structured data on the client)
  const alerts = [];
  (d.time || []).forEach((day, i) => {
    const p = d.precipitation_probability_max?.[i], r = d.precipitation_sum?.[i], wi = d.wind_speed_10m_max?.[i];
    if (p != null && p >= 70) alerts.push({ cls: "rain", day, msg: t("alert_rain").replace("{v}", p) });
    if (r != null && r >= 25) alerts.push({ cls: "heavy", day, msg: t("alert_heavy").replace("{v}", r) });
    if (wi != null && wi >= 35) alerts.push({ cls: "wind", day, msg: t("alert_wind").replace("{v}", wi) });
  });
  $("alerts").innerHTML = alerts.map(a => `<div class="alert ${a.cls}"><b>${esc(a.day)}</b> – ${esc(a.msg)}</div>`).join("");

  const labels = d.time || [];
  mkChart("tempChart", { type: "line", data: { labels, datasets: [
    { label: t("hi"), data: d.temperature_2m_max, borderColor: "#e65100", backgroundColor: "#e6510033", tension: .3 },
    { label: t("lo"), data: d.temperature_2m_min, borderColor: "#1565c0", backgroundColor: "#1565c033", tension: .3 }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: t("tempChart") } } } });
  mkChart("rainChart", { data: { labels, datasets: [
    { type: "bar", label: t("rainChart"), data: d.precipitation_sum, backgroundColor: "#42a5f5", yAxisID: "y" },
    { type: "line", label: t("rainProbChart"), data: d.precipitation_probability_max, borderColor: "#2e7d32", yAxisID: "y1", tension: .3 }] },
    options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true }, y1: { position: "right", min: 0, max: 100, grid: { drawOnChartArea: false } } } } });

  let rows = `<tr><th>${t("day")}</th><th>${t("hi")}</th><th>${t("lo")}</th><th>${t("rainMm")}</th><th>${t("rainP")}</th><th>${t("windKm")}</th><th>${t("uv")}</th><th>${t("et0")}</th></tr>`;
  labels.forEach((day, i) => {
    rows += `<tr><td>${esc(day)}</td><td>${fmt(d.temperature_2m_max?.[i], 1)}</td><td>${fmt(d.temperature_2m_min?.[i], 1)}</td><td>${fmt(d.precipitation_sum?.[i], 1)}</td><td>${fmt(d.precipitation_probability_max?.[i])}</td><td>${fmt(d.wind_speed_10m_max?.[i])}</td><td>${fmt(d.uv_index_max?.[i], 1)}</td><td>${fmt(d.et0_fao_evapotranspiration?.[i], 1)}</td></tr>`;
  });
  $("dailyTable").innerHTML = rows;
  $("wSource").textContent = w.source;
  $("wTime").textContent = new Date(w.fetched_at).toLocaleString(lang === "hi" ? "hi-IN" : "en-IN");
}

$("weatherForm").addEventListener("submit", async e => {
  e.preventDefault();
  const q = $("location").value.trim();
  if (!q) return setMsg("weatherMsg", t("enterLoc"), "err");
  setMsg("weatherMsg", t("loading"));
  try {
    S.weather = await api("/api/weather?location=" + encodeURIComponent(q));
    setMsg("weatherMsg", "");
    renderWeather();
    if ($("calCrop").value) buildCalendar(true); // forecast changed -> re-check calendar
  } catch (err) { setMsg("weatherMsg", err.message, "err"); }
});

$("fillWeather").addEventListener("click", () => {
  if (!S.weather) return setMsg("cropMsg", t("loadWeatherFirst"), "err");
  const d = S.weather.daily, h = S.weather.hourly;
  const avg = a => { const v = (a || []).filter(x => x != null); return v.length ? v.reduce((s, x) => s + x, 0) / v.length : null; };
  const tmax = avg(d.temperature_2m_max), tmin = avg(d.temperature_2m_min), hum = avg(h.relative_humidity_2m);
  const f = $("cropForm");
  if (tmax != null && tmin != null) f.temperature.value = ((tmax + tmin) / 2).toFixed(1);
  if (hum != null) f.humidity.value = Math.round(hum);
  setMsg("cropMsg", t("filled"), "ok");
});

/* ---------- crops ---------- */
function reasonText(r) { return T[lang].reasons[r] || r; }
function renderRecs() {
  const R = S.recs;
  const first = R.recommendations[0];
  const baseline = first && first.method === "baseline";
  $("cropResults").innerHTML = `<p class="muted small">${t("method")}: <b>${esc(R.method)}</b></p>` +
    R.recommendations.map((r, i) => `
    <div class="card rec">
      <div class="rec-head"><h3>#${i + 1} ${esc(cropName(r.crop))}</h3>
        ${r.score != null ? `<span class="score">${baseline ? t("scoreBase") : t("score")}: ${r.score}%</span>` : ""}</div>
      <div>
        <span class="tag ${r.within_budget ? "good" : "bad"}">${r.within_budget ? t("withinBudget") : t("overBudget")}</span>
        <span class="tag">${t("season")}: ${esc(seasonName(r.season))}</span>
        <span class="tag">${t("days")}: ${r.days}</span>
        <span class="tag">${t("water")}: ${esc(t(r.water))}</span>
      </div>
      <div class="grid stats">
        <div class="stat"><b>${inr(r.cost)}</b><span>${t("cost")}</span></div>
        <div class="stat"><b>${inr(r.gross)}</b><span>${t("gross")}</span></div>
        <div class="stat"><b class="${r.net >= 0 ? "pos" : "neg"}">${inr(r.net)}</b><span>${t("net")}</span></div>
      </div>
      <div><b>${t("why")}</b><ul>${r.reasons.map(x => `<li>${esc(reasonText(x))}</li>`).join("")}</ul></div>
    </div>`).join("") +
    `<p class="muted small">${t("notice")}</p>`;
}
$("cropForm").addEventListener("submit", async e => {
  e.preventDefault();
  const fd = Object.fromEntries(new FormData(e.target).entries());
  setMsg("cropMsg", t("loading"));
  try {
    S.recs = await api("/api/recommend", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(fd) });
    setMsg("cropMsg", "");
    renderRecs();
  } catch (err) { setMsg("cropMsg", err.message, "err"); }
});

/* ---------- crop selects (simulator + calendar) ---------- */
function fillCropSelects() {
  if (!S.crops) return;
  const names = Object.keys(S.crops).sort((a, b) => cropName(a).localeCompare(cropName(b), lang));
  const simSel = $("simCrops"), calSel = $("calCrop");
  const chosen = new Set([...simSel.selectedOptions].map(o => o.value));
  const calVal = calSel.value;
  const firstTime = simSel.options.length === 0;
  simSel.innerHTML = names.map(c => `<option value="${c}">${esc(cropName(c))}</option>`).join("");
  calSel.innerHTML = names.map(c => `<option value="${c}">${esc(cropName(c))}</option>`).join("");
  [...simSel.options].forEach(o => { o.selected = firstTime ? ["rice", "maize", "chickpea"].includes(o.value) : chosen.has(o.value); });
  if (calVal) calSel.value = calVal;
}

/* ---------- simulator ---------- */
function renderSim() {
  if (!S.crops) return;
  const land = Math.max(0.1, parseFloat($("simLand").value) || 1);
  const pp = +$("simPrice").value, cp = +$("simCost").value, yp = +$("simYield").value;
  $("simPriceV").textContent = (pp > 0 ? "+" : "") + pp + "%";
  $("simCostV").textContent = (cp > 0 ? "+" : "") + cp + "%";
  $("simYieldV").textContent = (yp > 0 ? "+" : "") + yp + "%";
  const picked = [...$("simCrops").selectedOptions].map(o => o.value);
  if (!picked.length) { $("simTable").innerHTML = `<tr><td>${t("simPick")}</td></tr>`; if (S.charts.simChart) { S.charts.simChart.destroy(); delete S.charts.simChart; } return; }
  const rows = picked.map(c => {
    const e = S.crops[c];
    const cost = e.cost * (1 + cp / 100) * land;
    const gross = e.yield_t * (1 + yp / 100) * e.price * (1 + pp / 100) * land;
    return { c, cost, gross, net: gross - cost, e };
  });
  mkChart("simChart", { type: "bar", data: { labels: rows.map(r => cropName(r.c)), datasets: [
    { label: t("costLbl"), data: rows.map(r => Math.round(r.cost)), backgroundColor: "#ef9a9a" },
    { label: t("grossLbl"), data: rows.map(r => Math.round(r.gross)), backgroundColor: "#90caf9" },
    { label: t("netLbl"), data: rows.map(r => Math.round(r.net)), backgroundColor: "#66bb6a" }] },
    options: { responsive: true, maintainAspectRatio: false, scales: { y: { title: { display: true, text: t("costAxis") } } } } });
  $("simTable").innerHTML = `<tr><th>${t("crop")}</th><th>${t("cost")}</th><th>${t("gross")}</th><th>${t("simNet")}</th><th>${t("days")}</th><th>${t("water")}</th><th>${t("season")}</th></tr>` +
    rows.map(r => `<tr><td>${esc(cropName(r.c))}</td><td>${inr(r.cost)}</td><td>${inr(r.gross)}</td><td class="${r.net >= 0 ? "pos" : "neg"}">${inr(r.net)}</td><td>${r.e.days}</td><td>${esc(t(r.e.water))}</td><td>${esc(seasonName(r.e.season))}</td></tr>`).join("");
}
["simCrops", "simLand", "simPrice", "simCost", "simYield"].forEach(id => $(id).addEventListener("input", renderSim));

/* ---------- calendar ---------- */
function renderCalendar() {
  const C = S.cal;
  const tl = C.timeline.map(s => `<li><b>${esc(s.date)}</b> <span class="muted">(${s.day >= 0 ? "+" : ""}${s.day} ${lang === "hi" ? "दिन" : "d"})</span><br>${esc(T[lang].stage[s.stage] || s.task)}</li>`).join("");
  const adv = C.forecast_advice.map(a => `
    <div class="card">
      <b>${esc(a.date)}</b> <span class="muted small">${t("maxT")} ${fmt(a.tmax, 0)}°C · ${t("rainW")} ${fmt(a.rain_mm, 1)} mm (${fmt(a.rain_prob)}%) · ${t("windW")} ${fmt(a.wind)} km/h</span>
      <div>${a.items.map(i => `<div><span class="st ${i.status}">${t("st_" + i.status)}</span>${esc(T[lang].adv[i.key] || i.key)}</div>`).join("") || "–"}</div>
    </div>`).join("");
  $("calResults").innerHTML = `<div class="card"><h3>${cropName(C.crop)} – ${t("timeline")}</h3><ul class="timeline">${tl}</ul></div>
    <h3>${t("next7")}</h3>${adv}`;
}
async function buildCalendar(auto) {
  const crop = $("calCrop").value;
  if (!crop) return setMsg("calMsg", t("calNeedCrop"), "err");
  if (!S.weather) return setMsg("calMsg", t("calNeedWeather"), "err");
  setMsg("calMsg", t("loading"));
  try {
    S.cal = await api("/api/calendar", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ crop, sow_date: $("calDate").value, daily: S.weather.daily }) });
    const sig = JSON.stringify(S.cal.forecast_advice.map(a => a.items.map(i => i.key)));
    const changed = S.lastCalSig && S.lastCalSig !== sig;
    S.lastCalSig = sig;
    setMsg("calMsg", (changed ? t("changed") + ". " : "") + t("calDone"), "ok");
    renderCalendar();
  } catch (err) { setMsg("calMsg", err.message, "err"); }
}
$("calBtn").addEventListener("click", () => buildCalendar(false));

/* ---------- init ---------- */
$("calDate").value = new Date().toISOString().slice(0, 10);
api("/api/crops").then(j => { S.crops = j.crops; fillCropSelects(); renderSim(); }).catch(() => {});
applyLang();
})();
