(() => {
"use strict";

const TXT = {
  hi: {
    brand: "किसान मित्र", hero: "आपके खेत के लिए सही फसल जानें",
    s1: "1️⃣ आपकी जगह", gps: "📍 मेरी जगह इस्तेमाल करें",
    privacy: "आपकी जगह सिर्फ़ मौसम देखने के लिए इस्तेमाल होती है। इसे सेव नहीं किया जाता।",
    typePlace: "या अपने गाँव/शहर का नाम लिखें", placePh: "जैसे: जयपुर", ok: "ठीक है",
    s2: "2️⃣ आपकी मिट्टी कैसी है?",
    soilBlack: "⚫ काली मिट्टी", soilRed: "🔴 लाल मिट्टी", soilSandy: "🏜️ रेतीली (बलुई)", soilLoam: "🟤 दोमट (भुरभुरी)", soilClay: "🏺 चिकनी", soilUnknown: "❓ पता नहीं",
    s3: "3️⃣ सिंचाई के लिए पानी कितना है?",
    waterPlenty: "💧💧💧 खूब पानी", waterSome: "💧💧 थोड़ा पानी", waterLittle: "💧 बहुत कम (बारिश के भरोसे)",
    s4: "4️⃣ खेती में कितना पैसा लगा सकते हैं? (एक एकड़ के लिए)",
    budLow: "💵 कम", budMed: "💰 ठीक-ठाक", budHigh: "💰💰 ज़्यादा",
    go: "🌱 बताइए क्या उगाऊँ", adviceTitle: "किसान मित्र की सलाह", listen: "🔊 सुनिए", stop: "⏹️ रोकिए",
    weekTitle: "📅 इस हफ़्ते का मौसम", rainNote: "💧 का मतलब है बारिश की संभावना",
    bestTitle: "⭐ आपके लिए सबसे अच्छी फसल", othersTitle: "👍 दूसरे विकल्प", tipsTitle: "🚜 इस हफ़्ते खेत पर क्या करें",
    again: "🔄 दोबारा पूछें", expert: "विस्तृत जानकारी (विशेषज्ञों के लिए)",
    locFound: "✅ आपकी जगह मिल गई", locTyped: "✅ जगह: ",
    locDenied: "लोकेशन की अनुमति नहीं मिली। कृपया ऊपर अपने गाँव/शहर का नाम लिखें।",
    locFail: "आपकी जगह नहीं मिल सकी। कृपया अपने गाँव/शहर का नाम लिखें।",
    locNone: "आपके फ़ोन/ब्राउज़र में लोकेशन उपलब्ध नहीं है। कृपया अपने गाँव/शहर का नाम लिखें।",
    locWait: "⏳ आपकी जगह ढूँढ रहा हूँ…", needLoc: "पहले अपनी जगह बताइए (ऊपर का बटन दबाएँ)।",
    thinking: "आपके खेत के लिए सोच रहा हूँ…", generic: "कुछ गड़बड़ हो गई। कृपया फिर कोशिश करें।",
    chatTitle: "💬 अपना सवाल पूछिए", chatHelp: "खेती से जुड़ा कोई भी सवाल बोलकर या लिखकर पूछें।", chatPh: "यहाँ लिखें…", chatSend: "भेजें",
    chatWait: "सोच रहा हूँ…", chatSpeak: "🔊 सुनिए", micListen: "बोलिए…", micFail: "आवाज़ समझ नहीं आई। कृपया लिखकर पूछें।",
    sug: ["गेहूँ कब बोऊँ?", "फसल में कीड़े लग गए तो क्या करूँ?", "कम पानी में क्या करूँ?"],
    helpTitle: "📞 किसान कॉल सेंटर (मुफ़्त)", helpText: "खेती की किसी भी समस्या पर विशेषज्ञ से अपनी भाषा में बात करें। रोज़ सुबह 6 से रात 10 बजे तक।",
    helpFree: "यह नंबर पूरे भारत में मुफ़्त है (भारत सरकार, कृषि मंत्रालय)।"
  },
  en: {
    brand: "KisanMitra", hero: "Find the right crop for your farm",
    s1: "1️⃣ Your place", gps: "📍 Use my location",
    privacy: "Your location is only used to check the weather. It is not saved.",
    typePlace: "Or type your village/town", placePh: "for example: Jaipur", ok: "OK",
    s2: "2️⃣ What is your soil like?",
    soilBlack: "⚫ Black soil", soilRed: "🔴 Red soil", soilSandy: "🏜️ Sandy", soilLoam: "🟤 Loamy (crumbly)", soilClay: "🏺 Clay (sticky)", soilUnknown: "❓ Not sure",
    s3: "3️⃣ How much water do you have for irrigation?",
    waterPlenty: "💧💧💧 Plenty", waterSome: "💧💧 Some", waterLittle: "💧 Very little (only rain)",
    s4: "4️⃣ How much money can you spend on farming? (for one acre)",
    budLow: "💵 Little", budMed: "💰 Medium", budHigh: "💰💰 More",
    go: "🌱 Tell me what to grow", adviceTitle: "KisanMitra's advice", listen: "🔊 Listen", stop: "⏹️ Stop",
    weekTitle: "📅 Weather this week", rainNote: "💧 means rain is likely",
    bestTitle: "⭐ Best crop for you", othersTitle: "👍 Other choices", tipsTitle: "🚜 What to do on the farm this week",
    again: "🔄 Ask again", expert: "Detailed view (for experts)",
    locFound: "✅ Your location was found", locTyped: "✅ Place: ",
    locDenied: "Location permission was not given. Please type your village/town above.",
    locFail: "Could not find your location. Please type your village/town.",
    locNone: "Location is not available on this phone/browser. Please type your village/town.",
    locWait: "⏳ Finding your location…", needLoc: "Please tell us your place first (press the button above).",
    thinking: "Thinking about your farm…", generic: "Something went wrong. Please try again.",
    chatTitle: "💬 Ask your question", chatHelp: "Ask anything about farming - by speaking or typing.", chatPh: "Type here…", chatSend: "Send",
    chatWait: "Thinking…", chatSpeak: "🔊 Listen", micListen: "Speak now…", micFail: "Could not understand. Please type your question.",
    sug: ["When should I sow wheat?", "Pests attacked my crop. What should I do?", "What if I have very little water?"],
    helpTitle: "📞 Kisan Call Centre (free)", helpText: "Talk to an expert in your own language about any farming problem. Every day, 6 am to 10 pm.",
    helpFree: "This number is free across India (Government of India, Ministry of Agriculture)."
  }
};
const SPEECH_LANG = { hi: "hi-IN", en: "en-IN" };
const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const S = { lang: "hi", loc: null, choice: { soil: "unknown", water: "some", budget: "medium" }, res: null, busy: false, timer: null, seq: 0, chat: [], chatOn: false, chatBusy: false };
try {
  const l = localStorage.getItem("kf_lang"); if (l === "hi" || l === "en") S.lang = l;
  const c = JSON.parse(localStorage.getItem("kf_choice") || "null"); if (c && c.soil && c.water && c.budget) S.choice = c;
} catch (e) {}
const t = k => TXT[S.lang][k] ?? TXT.hi[k] ?? k;
const canSpeak = "speechSynthesis" in window && "SpeechSynthesisUtterance" in window;

/* ---------- language + static text ---------- */
function applyLang() {
  document.documentElement.lang = S.lang;
  document.querySelectorAll("[data-i18n]").forEach(el => { el.textContent = t(el.dataset.i18n); });
  document.querySelectorAll("[data-i18n-ph]").forEach(el => { el.placeholder = t(el.dataset.i18nPh); });
  $("langBtn").textContent = S.lang === "hi" ? "English" : "हिंदी";
  $("listenBtn").classList.toggle("hidden", !canSpeak);
  if (S.loc) setStatus(S.loc.label ? t("locTyped") + S.loc.label : t("locFound"));
  if (S.res) renderResult();
  renderAskChips(); renderChat();
}
$("langBtn").addEventListener("click", () => {
  stopSpeech();
  S.lang = S.lang === "hi" ? "en" : "hi";
  try { localStorage.setItem("kf_lang", S.lang); } catch (e) {}
  applyLang();
});

/* ---------- tiles ---------- */
function syncTiles() {
  document.querySelectorAll(".tiles").forEach(g => {
    const val = S.choice[g.dataset.group];
    g.querySelectorAll(".tile").forEach(b => { b.setAttribute("role", "radio"); b.setAttribute("aria-checked", String(b.dataset.value === val)); });
  });
}
document.querySelectorAll(".tiles").forEach(g => g.addEventListener("click", e => {
  const b = e.target.closest(".tile"); if (!b) return;
  S.choice[g.dataset.group] = b.dataset.value;
  try { localStorage.setItem("kf_choice", JSON.stringify(S.choice)); } catch (e2) {}
  syncTiles();
  if (S.loc) { clearTimeout(S.timer); S.timer = setTimeout(() => ask(false), 400); } // refresh advice after a change
}));

/* ---------- location ---------- */
function setStatus(text, err) { const el = $("locStatus"); el.textContent = text || ""; el.className = "status" + (err ? " err" : ""); }
function setMsg(text, err) { const el = $("msg"); el.textContent = text || ""; el.className = "msg" + (err ? " err" : ""); }

$("gpsBtn").addEventListener("click", () => {
  if (!navigator.geolocation) { setStatus(t("locNone"), true); $("placeInput").focus(); return; }
  setStatus(t("locWait"));
  navigator.geolocation.getCurrentPosition(
    pos => {
      S.loc = { lat: pos.coords.latitude, lon: pos.coords.longitude };
      setStatus(t("locFound"));
      ask(true);
    },
    err => {
      setStatus(err && err.code === 1 ? t("locDenied") : t("locFail"), true);
      $("placeInput").focus();
    },
    { enableHighAccuracy: false, timeout: 15000, maximumAge: 600000 }
  );
});
$("placeForm").addEventListener("submit", e => {
  e.preventDefault();
  const p = $("placeInput").value.trim();
  if (!p) return;
  S.loc = { place: p, label: p };
  setStatus(t("locTyped") + p);
  ask(true);
});
$("goBtn").addEventListener("click", () => ask(true));
$("againBtn").addEventListener("click", () => { stopSpeech(); window.scrollTo({ top: 0, behavior: "smooth" }); });

/* ---------- ask the server ---------- */
async function ask(scroll) {
  if (!S.loc) { setMsg(t("needLoc"), true); return; }
  const mySeq = ++S.seq;
  setMsg("⏳ " + t("thinking"));
  $("goBtn").disabled = true;
  try {
    const r = await fetch("/api/advice", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...S.loc, ...S.choice }) });
    let j = {}; try { j = await r.json(); } catch (e) {}
    if (mySeq !== S.seq) return; // a newer request replaced this one
    if (!r.ok) { setMsg((j.error && (j.error[S.lang] || j.error.en)) || t("generic"), true); return; }
    S.res = j;
    setMsg("");
    renderResult();
    if (scroll) $("result").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (e) {
    if (mySeq === S.seq) setMsg(t("generic"), true);
  } finally {
    if (mySeq === S.seq) $("goBtn").disabled = false;
  }
}

/* ---------- show the answer ---------- */
function renderResult() {
  const R = S.res, X = R.text[S.lang];
  $("result").classList.remove("hidden");
  $("bubble").innerHTML = X.paragraphs.map(p => `<p>${esc(p)}</p>`).join("");
  $("week").innerHTML = R.week.map(w => `<div class="wd${w.rain ? " rain" : ""}"><b>${esc(S.lang === "hi" ? w.day_hi : w.day_en)}</b><span>${w.emoji}</span><i>${w.rain ? "💧" : ""}</i></div>`).join("");
  $("bestEmoji").textContent = X.best.emoji;
  $("bestName").textContent = X.best.name;
  $("chips").innerHTML = X.best.chips.map(c => `<span class="chip">${c.icon} ${esc(c.text)}</span>`).join("");
  $("reasons").innerHTML = X.best.reasons.map(r => `<li>${esc(r)}</li>`).join("");
  $("othersCard").classList.toggle("hidden", !X.others.length);
  $("others").innerHTML = X.others.map(o => `<div class="opt"><span class="e">${o.emoji}</span><div><b>${esc(o.name)}</b><span>${esc(o.line)}</span></div></div>`).join("");
  $("tips").innerHTML = X.tips.map(x => `<li><span class="ic">${x.icon}</span><span>${esc(x.text)}</span></li>`).join("");
  $("note").textContent = "";
}

/* ---------- read aloud ---------- */
function stopSpeech() {
  if (canSpeak) window.speechSynthesis.cancel();
  $("stopBtn").classList.add("hidden");
  $("listenBtn").classList.toggle("hidden", !canSpeak);
}
$("listenBtn").addEventListener("click", () => {
  if (!canSpeak || !S.res) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(S.res.text[S.lang].speech);
  u.lang = SPEECH_LANG[S.lang]; u.rate = 0.9;
  const done = () => { $("stopBtn").classList.add("hidden"); $("listenBtn").classList.remove("hidden"); };
  u.onend = done; u.onerror = done;
  $("listenBtn").classList.add("hidden");
  $("stopBtn").classList.remove("hidden");
  window.speechSynthesis.speak(u);
});
$("stopBtn").addEventListener("click", stopSpeech);

/* ---------- chat ---------- */
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
function chatContext() {
  if (!S.res) return "";
  const X = S.res.text[S.lang];
  return X.paragraphs.slice(0, 4).join(" ") + " " + X.tips.map(x => x.text).join(" ");
}
function renderAskChips() {
  const box = $("askChips");
  box.innerHTML = (t("sug") || []).map((q, i) => `<button type="button" data-q="${i}">${esc(q)}</button>`).join("");
  box.classList.toggle("hidden", S.chat.length > 0);
}
function renderChat() {
  $("chatLog").innerHTML = S.chat.map((m, i) => m.role === "user"
    ? `<div class="msg-b user">${esc(m.content)}</div>`
    : `<div class="msg-b bot${m.err ? " err" : ""}">${esc(m.content)}${canSpeak ? `<button type="button" class="spk" data-i="${i}">${t("chatSpeak")}</button>` : ""}</div>`).join("")
    + (S.chatBusy ? `<div class="msg-b bot">⏳ ${esc(t("chatWait"))}</div>` : "");
  const log = $("chatLog"); log.scrollTop = log.scrollHeight;
  $("askChips").classList.toggle("hidden", S.chat.length > 0);
}
async function sendChat(text) {
  text = (text || "").trim();
  if (!text || S.chatBusy) return;
  S.chat.push({ role: "user", content: text });
  $("chatInput").value = "";
  S.chatBusy = true; renderChat();
  try {
    const r = await fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: S.chat.map(m => ({ role: m.role, content: m.content })), context: chatContext(), lang: S.lang }) });
    let j = {}; try { j = await r.json(); } catch (e) {}
    if (r.ok && j.reply) S.chat.push({ role: "assistant", content: j.reply });
    else S.chat.push({ role: "assistant", err: true, content: (j.error && (j.error[S.lang] || j.error.en)) || t("generic") });
  } catch (e) {
    S.chat.push({ role: "assistant", err: true, content: t("generic") });
  }
  S.chatBusy = false; renderChat();
}
$("chatForm").addEventListener("submit", e => { e.preventDefault(); sendChat($("chatInput").value); });
$("askChips").addEventListener("click", e => { const b = e.target.closest("button"); if (b) sendChat(t("sug")[+b.dataset.q]); });
$("chatLog").addEventListener("click", e => {
  const b = e.target.closest(".spk"); if (!b || !canSpeak) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(S.chat[+b.dataset.i].content);
  u.lang = SPEECH_LANG[S.lang]; u.rate = 0.9; window.speechSynthesis.speak(u);
});
if (SR) {
  $("micBtn").classList.remove("hidden");
  $("micBtn").addEventListener("click", () => {
    const rec = new SR(); rec.lang = SPEECH_LANG[S.lang]; rec.interimResults = false; rec.maxAlternatives = 1;
    const btn = $("micBtn"); btn.classList.add("on"); $("chatInput").placeholder = t("micListen");
    const end = () => { btn.classList.remove("on"); $("chatInput").placeholder = t("chatPh"); };
    rec.onresult = ev => { end(); sendChat(ev.results[0][0].transcript); };
    rec.onerror = () => { end(); S.chat.push({ role: "assistant", err: true, content: t("micFail") }); renderChat(); };
    rec.onend = end;
    try { rec.start(); } catch (e) { end(); }
  });
}
fetch("/api/health").then(r => r.json()).then(h => { S.chatOn = !!h.chat_enabled; $("chatCard").classList.toggle("hidden", !S.chatOn); }).catch(() => {});

/* ---------- start ---------- */
syncTiles();
applyLang();
})();
