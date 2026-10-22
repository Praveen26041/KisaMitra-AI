from flask import Flask, render_template, request, jsonify
import requests, os, math, json
from datetime import datetime, timedelta
from pathlib import Path
import advice, chat

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = Path(os.environ.get("KM_MODEL", BASE_DIR / "models" / "crop_model.joblib"))
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

# Clearly labelled prototype planning assumptions (INR per acre, not official quotes).
# Replace these with district/state agricultural department or KVK figures before real-world use.
CROP_ECONOMICS = {
    "rice": {"cost": 24000, "yield_t": 2.4, "price": 23000, "days": 120, "water": "high", "season": "Kharif"},
    "maize": {"cost": 18000, "yield_t": 2.2, "price": 22000, "days": 100, "water": "medium", "season": "Kharif/Rabi"},
    "chickpea": {"cost": 14000, "yield_t": 0.9, "price": 55000, "days": 110, "water": "low", "season": "Rabi"},
    "kidneybeans": {"cost": 19000, "yield_t": 0.8, "price": 70000, "days": 105, "water": "medium", "season": "Kharif"},
    "pigeonpeas": {"cost": 16000, "yield_t": 0.8, "price": 70000, "days": 160, "water": "low", "season": "Kharif"},
    "mothbeans": {"cost": 10000, "yield_t": 0.6, "price": 70000, "days": 75, "water": "low", "season": "Kharif"},
    "mungbean": {"cost": 12000, "yield_t": 0.6, "price": 80000, "days": 70, "water": "low", "season": "Kharif/Summer"},
    "blackgram": {"cost": 13000, "yield_t": 0.7, "price": 75000, "days": 85, "water": "low", "season": "Kharif"},
    "lentil": {"cost": 13000, "yield_t": 0.8, "price": 65000, "days": 115, "water": "low", "season": "Rabi"},
    "pomegranate": {"cost": 45000, "yield_t": 8, "price": 30000, "days": 240, "water": "medium", "season": "Perennial"},
    "banana": {"cost": 70000, "yield_t": 25, "price": 12000, "days": 330, "water": "high", "season": "Perennial"},
    "mango": {"cost": 40000, "yield_t": 6, "price": 35000, "days": 365, "water": "medium", "season": "Perennial"},
    "grapes": {"cost": 100000, "yield_t": 10, "price": 40000, "days": 180, "water": "medium", "season": "Perennial"},
    "watermelon": {"cost": 22000, "yield_t": 18, "price": 12000, "days": 85, "water": "medium", "season": "Summer"},
    "muskmelon": {"cost": 22000, "yield_t": 12, "price": 15000, "days": 85, "water": "medium", "season": "Summer"},
    "apple": {"cost": 80000, "yield_t": 8, "price": 50000, "days": 365, "water": "medium", "season": "Perennial"},
    "orange": {"cost": 50000, "yield_t": 8, "price": 30000, "days": 365, "water": "medium", "season": "Perennial"},
    "papaya": {"cost": 35000, "yield_t": 25, "price": 12000, "days": 270, "water": "medium", "season": "Perennial"},
    "coconut": {"cost": 45000, "yield_t": 8, "price": 25000, "days": 365, "water": "medium", "season": "Perennial"},
    "cotton": {"cost": 25000, "yield_t": 1.8, "price": 65000, "days": 160, "water": "medium", "season": "Kharif"},
    "jute": {"cost": 20000, "yield_t": 1.0, "price": 50000, "days": 120, "water": "high", "season": "Kharif"},
    "coffee": {"cost": 65000, "yield_t": 0.8, "price": 180000, "days": 240, "water": "medium", "season": "Perennial"},
    # --- Crops that are NOT in the public training dataset. They are ranked by rule-based climate
    # profiles in advice.py (EXTRA_PROFILES), not by the ML model. Illustrative placeholders too. ---
    "wheat": {"cost": 20000, "yield_t": 1.8, "price": 22750, "days": 120, "water": "medium", "season": "Rabi"},
    "mustard": {"cost": 14000, "yield_t": 0.55, "price": 55000, "days": 120, "water": "low", "season": "Rabi"},
    "potato": {"cost": 55000, "yield_t": 8, "price": 12000, "days": 100, "water": "medium", "season": "Rabi"},
    "onion": {"cost": 45000, "yield_t": 8, "price": 15000, "days": 130, "water": "medium", "season": "Rabi"},
    "tomato": {"cost": 60000, "yield_t": 10, "price": 12000, "days": 110, "water": "medium", "season": "Rabi/Summer"},
    "soybean": {"cost": 15000, "yield_t": 0.8, "price": 45000, "days": 100, "water": "medium", "season": "Kharif"},
    "groundnut": {"cost": 25000, "yield_t": 0.9, "price": 60000, "days": 110, "water": "medium", "season": "Kharif"},
    "sorghum": {"cost": 12000, "yield_t": 0.9, "price": 31000, "days": 110, "water": "low", "season": "Kharif/Rabi"},
    "pearlmillet": {"cost": 10000, "yield_t": 0.8, "price": 26000, "days": 85, "water": "low", "season": "Kharif"},
    "okra": {"cost": 30000, "yield_t": 3, "price": 25000, "days": 90, "water": "medium", "season": "Kharif/Summer"},
}

def get_model():
    try:
        import joblib
        if MODEL_PATH.exists():
            return joblib.load(MODEL_PATH)
    except Exception:
        pass
    return None

def fallback_rank(values, n=3):
    """Transparent nearest-centroid baseline if no trained model is installed."""
    # Typical condition profiles approximated from the publicly used crop recommendation dataset.
    # This is a demo fallback, not a validated agronomic model.
    profiles = {
        "rice": [80, 45, 40, 24, 82, 6.3, 230],
        "maize": [75, 48, 20, 23, 66, 6.2, 85],
        "chickpea": [40, 68, 80, 19, 17, 6.5, 80],
        "kidneybeans": [20, 67, 20, 20, 22, 5.7, 105],
        "pigeonpeas": [20, 68, 20, 28, 48, 5.8, 150],
        "mothbeans": [20, 50, 20, 29, 53, 6.8, 50],
        "mungbean": [20, 48, 20, 28, 85, 6.7, 50],
        "blackgram": [40, 60, 20, 29, 65, 7.1, 70],
        "lentil": [20, 68, 20, 23, 64, 6.9, 45],
        "pomegranate": [20, 20, 40, 22, 90, 6.4, 110],
        "banana": [100, 80, 50, 27, 80, 6.0, 110],
        "mango": [20, 20, 30, 31, 50, 5.8, 95],
        "grapes": [20, 130, 200, 24, 82, 6.0, 70],
        "watermelon": [100, 20, 50, 26, 85, 6.5, 50],
        "muskmelon": [100, 20, 50, 28, 90, 6.4, 30],
        "apple": [20, 130, 200, 22, 90, 6.0, 110],
        "orange": [20, 20, 10, 23, 92, 7.0, 110],
        "papaya": [50, 50, 50, 33, 90, 6.7, 150],
        "coconut": [20, 10, 30, 27, 95, 5.9, 175],
        "cotton": [120, 45, 20, 24, 80, 6.9, 80],
        "jute": [80, 45, 40, 25, 80, 6.7, 175],
        "coffee": [100, 20, 30, 25, 58, 6.8, 160],
    }
    # Normalize distances by broad feature ranges to avoid units dominating.
    scales = [100, 100, 200, 20, 100, 5, 300]
    scores = []
    for crop, profile in profiles.items():
        d = math.sqrt(sum(((float(values[i]) - profile[i]) / scales[i]) ** 2 for i in range(7)))
        scores.append((crop, d))
    scores.sort(key=lambda x: x[1])
    # Sharper kernel weights: crops whose typical conditions are close to the real conditions
    # get most of the weight. Still a ranking score, explicitly not a calibrated probability.
    sigma = 0.2
    raw = [math.exp(-((d / sigma) ** 2)) for _, d in scores]
    total = sum(raw) or 1.0
    return [{"crop": c, "score": round((r / total) * 100), "method": "baseline"}
            for (c, _), r in list(zip(scores, raw))[:n]]

def recommend(values, n=3):
    model = get_model()
    if model is not None:
        import pandas as pd
        row = pd.DataFrame([[values[k] for k in FEATURES]], columns=FEATURES)
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(row)[0]
            classes = list(model.classes_)
            order = sorted(range(len(probs)), key=lambda i: probs[i], reverse=True)[:n]
            return [{"crop": str(classes[i]), "score": round(float(probs[i]) * 100), "method": "ml"} for i in order]
        pred = str(model.predict(row)[0])
        return [{"crop": pred, "score": None, "method": "ml"}]
    return fallback_rank([values[k] for k in FEATURES], n)

def weather_code_label(code):
    if code is None: return "Unavailable"
    if code == 0: return "Clear sky"
    if code in [1, 2, 3]: return "Mainly clear / cloudy"
    if code in [45, 48]: return "Fog"
    if code in [51, 53, 55, 56, 57]: return "Drizzle"
    if code in [61, 63, 65, 66, 67]: return "Rain"
    if code in [71, 73, 75, 77]: return "Snow"
    if code in [80, 81, 82]: return "Rain showers"
    if code in [85, 86]: return "Snow showers"
    if code in [95, 96, 99]: return "Thunderstorm"
    return "Mixed conditions"

@app.get("/")
def index():
    # Simple farmer screen: big buttons, plain words, read-aloud.
    return render_template("farmer.html")

@app.get("/expert")
def expert():
    # Detailed screen with numbers, charts, simulator and calendar (for officers / judges).
    return render_template("index.html")

def _err(en, hi, code):
    return jsonify({"error": {"en": en, "hi": hi}}), code

@app.post("/api/advice")
def api_advice():
    """Location + 3 simple answers -> plain-language advice in English and Hindi."""
    try:
        data = request.get_json(force=True) or {}
        lat, lon = data.get("lat"), data.get("lon")
        place = str(data.get("place") or "").strip()[:80]
        name = None
        if lat is None or lon is None:
            if not place:
                return _err("Please allow location or type your village/town.",
                            "कृपया लोकेशन की अनुमति दें या अपना गाँव/शहर लिखें।", 400)
            geo = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                               params={"name": place, "count": 1, "language": "en", "format": "json"}, timeout=10)
            geo.raise_for_status()
            results = geo.json().get("results", [])
            if not results:
                return _err("We could not find that place. Try a nearby town or district.",
                            "यह जगह नहीं मिली। पास के शहर या ज़िले का नाम लिखकर देखें।", 404)
            lat, lon, name = results[0]["latitude"], results[0]["longitude"], results[0].get("name")
        lat, lon = float(lat), float(lon)
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return _err("That location is not valid.", "यह लोकेशन सही नहीं है।", 400)
        forecast = advice.fetch_forecast(lat, lon)
        rain_monthly = advice.fetch_recent_rain_monthly(lat, lon)
        if name is None:
            name = advice.reverse_place(lat, lon)
        result = advice.build_advice(CROP_ECONOMICS, recommend, build_calendar, forecast, rain_monthly, name,
                                     data.get("soil"), data.get("water"), data.get("budget"), lat, lon)
        return jsonify(result)
    except requests.RequestException:
        return _err("Weather could not be loaded. Please check your internet and try again.",
                    "मौसम नहीं मिल सका। कृपया इंटरनेट जाँचकर फिर कोशिश करें।", 502)
    except (TypeError, ValueError):
        return _err("Something looks wrong with the information. Please try again.",
                    "जानकारी में कुछ गड़बड़ है। कृपया फिर कोशिश करें।", 400)
    except Exception:
        app.logger.exception("Advice failed")
        return _err("Sorry, something went wrong. Please try again.",
                    "माफ़ कीजिए, कुछ गड़बड़ हो गई। कृपया फिर कोशिश करें।", 500)

@app.get("/api/weather")
def api_weather():
    location = request.args.get("location", "").strip()
    if not location:
        return jsonify({"error": "Enter a town, city, or district."}), 400
    try:
        geo = requests.get("https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1, "language": "en", "format": "json"}, timeout=10)
        geo.raise_for_status()
        results = geo.json().get("results", [])
        if not results:
            return jsonify({"error": "Location not found. Try a nearby city or district."}), 404
        place = results[0]
        lat, lon = place["latitude"], place["longitude"]
        params = {
            "latitude": lat, "longitude": lon, "timezone": "auto",
            "forecast_days": 7,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m",
            "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m,cloud_cover,et0_fao_evapotranspiration",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,daylight_duration,uv_index_max,precipitation_sum,rain_sum,precipitation_probability_max,wind_speed_10m_max,et0_fao_evapotranspiration",
        }
        res = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=15)
        res.raise_for_status()
        data = res.json()
        current = data.get("current", {})
        current["description"] = weather_code_label(current.get("weather_code"))
        daily = data.get("daily", {})
        alerts = []
        probs = daily.get("precipitation_probability_max", [])
        rains = daily.get("precipitation_sum", [])
        winds = daily.get("wind_speed_10m_max", [])
        for i, day in enumerate(daily.get("time", [])):
            p = probs[i] if i < len(probs) else None
            r = rains[i] if i < len(rains) else None
            w = winds[i] if i < len(winds) else None
            if p is not None and p >= 70:
                alerts.append({"type": "rain", "day": day, "message": f"High rain chance ({p}%). Review irrigation and avoid spraying before rain."})
            if r is not None and r >= 25:
                alerts.append({"type": "heavy", "day": day, "message": f"Forecast rainfall {r} mm. Check drainage and field access."})
            if w is not None and w >= 35:
                alerts.append({"type": "wind", "day": day, "message": f"Strong wind forecast ({w} km/h). Secure light structures and review spraying."})
        return jsonify({
            "location": {"name": place.get("name"), "admin1": place.get("admin1"), "country": place.get("country"),
                         "latitude": lat, "longitude": lon, "timezone": data.get("timezone")},
            "current": current, "hourly": data.get("hourly", {}), "daily": daily,
            "alerts": alerts, "fetched_at": datetime.now().astimezone().isoformat(),
            "source": "Open-Meteo Forecast API"
        })
    except requests.RequestException:
        return jsonify({"error": "Weather service could not be reached. Check internet and try again."}), 502
    except Exception:
        app.logger.exception("Weather endpoint failed")
        return jsonify({"error": "Unexpected weather error. Please try again."}), 500

@app.post("/api/recommend")
def api_recommend():
    try:
        data = request.get_json(force=True)
        values = {
            "N": float(data["N"]), "P": float(data["P"]), "K": float(data["K"]),
            "temperature": float(data["temperature"]), "humidity": float(data["humidity"]),
            "ph": float(data["ph"]), "rainfall": float(data["rainfall"])
        }
        if not (0 <= values["N"] <= 150 and 0 <= values["P"] <= 150 and 0 <= values["K"] <= 210):
            return jsonify({"error": "N, P and K values are outside the supported demo ranges."}), 400
        if not (0 <= values["temperature"] <= 55 and 0 <= values["humidity"] <= 100 and 3 <= values["ph"] <= 10 and 0 <= values["rainfall"] <= 500):
            return jsonify({"error": "Check temperature, humidity, pH and rainfall values."}), 400
        land = max(0.1, min(10000, float(data.get("land", 1))))
        budget = max(0, float(data.get("budget", 30000)))
        irrigation = data.get("irrigation", "available")
        recs = recommend(values)
        output = []
        for rec in recs:
            crop = rec["crop"].lower().replace(" ", "")
            econ = CROP_ECONOMICS.get(crop, {"cost": 20000, "yield_t": 1.2, "price": 25000, "days": 120, "water": "medium", "season": "Varies"})
            total_cost = round(econ["cost"] * land)
            gross = round(econ["yield_t"] * econ["price"] * land)
            # Planning-only, conservative cost-over-budget check; yield/revenue are assumptions, not predictions.
            net = gross - total_cost
            reasons = []
            if values["rainfall"] >= 180: reasons.append("High rainfall input favours crops that can use wetter conditions; verify drainage.")
            elif values["rainfall"] <= 70: reasons.append("Lower rainfall input makes water planning especially important.")
            if 5.5 <= values["ph"] <= 7.5: reasons.append("Entered soil pH is within a broadly common crop-growing range.")
            if irrigation == "limited" and econ["water"] == "high": reasons.append("Water demand may conflict with your limited irrigation.")
            if total_cost > budget: reasons.append("Estimated cultivation cost exceeds the entered budget.")
            if not reasons: reasons.append("This crop ranked near the top for the entered soil and climate values.")
            output.append({
                "crop": rec["crop"], "score": rec["score"], "method": rec["method"],
                "cost": total_cost, "gross": gross, "net": net, "days": econ["days"],
                "water": econ["water"], "season": econ["season"], "reasons": reasons,
                "within_budget": total_cost <= budget
            })
        method = "Trained ML model (from dataset)" if output and output[0]["method"] == "ml" else "transparent baseline (model not trained)"
        return jsonify({"recommendations": output, "method": method, "land": land, "budget": budget,
                        "notice": "Economics are illustrative planning assumptions, not guaranteed yield, market price, or profit. Confirm locally with a KVK/agriculture officer."})
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Please fill all soil and farm fields with valid numbers."}), 400
    except Exception:
        app.logger.exception("Recommendation failed")
        return jsonify({"error": "Could not create recommendations. Check the inputs."}), 500

CHAT_ERRORS = {
    "off": (("Chat is not switched on yet. You can call the free Kisan Call Centre: 1800-180-1551.",
             "चैट अभी चालू नहीं है। आप मुफ़्त किसान कॉल सेंटर 1800-180-1551 पर बात कर सकते हैं।"), 503),
    "busy": (("Too many people are asking right now. Please try again in a minute.",
              "अभी बहुत लोग पूछ रहे हैं। कृपया एक मिनट बाद फिर कोशिश करें।"), 503),
    "rate": (("You have asked many questions. Please wait a little, or call the Kisan Call Centre: 1800-180-1551.",
              "आपने काफ़ी सवाल पूछ लिए हैं। थोड़ी देर रुकें, या किसान कॉल सेंटर 1800-180-1551 पर बात करें।"), 429),
    "bad": (("Please type your question again.", "कृपया अपना सवाल दोबारा लिखें।"), 400),
    "fail": (("Sorry, I could not answer right now. Please try again, or call 1800-180-1551.",
              "माफ़ कीजिए, अभी जवाब नहीं दे सका। फिर कोशिश करें, या 1800-180-1551 पर बात करें।"), 502),
}

@app.post("/api/chat")
def api_chat():
    """Free-form farmer question -> short plain-language answer (needs ANTHROPIC_API_KEY on the server)."""
    def fail(kind):
        (en, hi), code = CHAT_ERRORS[kind]
        return _err(en, hi, code)
    try:
        if not chat.enabled():
            return fail("off")
        data = request.get_json(force=True, silent=True) or {}
        msgs = chat.clean_messages(data.get("messages"))
        ip = (request.headers.get("X-Forwarded-For", request.remote_addr or "") or "").split(",")[0].strip()
        if not chat.allow(ip):
            return fail("rate")
        lang = "en" if data.get("lang") == "en" else "hi"
        reply = chat.ask(msgs, lang, str(data.get("context") or ""))
        return jsonify({"reply": reply})
    except chat.ChatError as e:
        return fail(e.kind)
    except Exception:
        app.logger.exception("Chat failed")
        return fail("fail")

@app.get("/api/crops")
def api_crops():
    return jsonify({"crops": CROP_ECONOMICS})

def build_calendar(crop, sow_date, daily):
    """Weather-adaptive plan: a fixed crop-stage timeline plus per-day advice for the 7-day forecast."""
    econ = CROP_ECONOMICS.get(crop)
    if not econ:
        raise ValueError("unknown crop")
    total = econ["days"]
    stages = [
        ("prep", -3, "Land preparation and basal manure"),
        ("sowing", 0, "Sowing / transplanting"),
        ("irrigation", 7, "First irrigation check"),
        ("weeding", int(total * 0.2), "First weeding"),
        ("fertilizer", int(total * 0.3), "Top-dress fertilizer (split dose)"),
        ("pest", int(total * 0.45), "Pest and disease scouting"),
        ("weeding", int(total * 0.5), "Second weeding"),
        ("harvest", total, "Expected harvest window"),
    ]
    timeline = [{"stage": k, "date": (sow_date + timedelta(days=d)).isoformat(), "day": d, "task": t}
                for k, d, t in stages]
    days = daily.get("time", [])
    def g(key, i):
        arr = daily.get(key, [])
        return arr[i] if i < len(arr) else None
    advice = []
    for i, day in enumerate(days):
        p, r, w = g("precipitation_probability_max", i), g("precipitation_sum", i), g("wind_speed_10m_max", i)
        tmax, et0 = g("temperature_2m_max", i), g("et0_fao_evapotranspiration", i)
        items = []
        wet = (p is not None and p >= 70) or (r is not None and r >= 10)
        if wet:
            items.append({"status": "hold", "key": "spray_hold"})
            items.append({"status": "hold", "key": "fert_hold"})
            items.append({"status": "skip", "key": "irrigation_skip"})
        else:
            if w is None or w < 25:
                items.append({"status": "go", "key": "spray_ok"})
            else:
                items.append({"status": "hold", "key": "wind_hold"})
            if et0 is not None and et0 >= 5 and econ["water"] != "low":
                items.append({"status": "go", "key": "irrigate_high_et"})
        if r is not None and r >= 25:
            items.append({"status": "warn", "key": "drainage"})
        if tmax is not None and tmax >= 40:
            items.append({"status": "warn", "key": "heat"})
        if tmax is not None and tmax <= 5:
            items.append({"status": "warn", "key": "cold"})
        advice.append({"date": day, "tmax": tmax, "rain_mm": r, "rain_prob": p, "wind": w, "et0": et0, "items": items})
    return {"crop": crop, "sow_date": sow_date.isoformat(), "timeline": timeline, "forecast_advice": advice}

@app.post("/api/calendar")
def api_calendar():
    try:
        data = request.get_json(force=True)
        crop = str(data["crop"]).lower().replace(" ", "")
        try:
            sow = datetime.strptime(data.get("sow_date", ""), "%Y-%m-%d").date()
        except ValueError:
            sow = datetime.now().date()
        daily = data.get("daily") or {}
        return jsonify(build_calendar(crop, sow, daily))
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Choose a crop and load the weather first."}), 400
    except Exception:
        app.logger.exception("Calendar failed")
        return jsonify({"error": "Could not build the calendar."}), 500

@app.get("/api/health")
def health():
    metrics = None
    try:
        mp = MODEL_PATH.parent / "metrics.json"
        if mp.exists():
            metrics = json.loads(mp.read_text(encoding="utf-8"))
    except Exception:
        pass
    return jsonify({"status": "ok", "ml_model_ready": MODEL_PATH.exists(), "metrics": metrics, "chat_enabled": chat.enabled()})

if __name__ == "__main__":
    app.run(debug=True)
