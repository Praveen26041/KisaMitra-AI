"""Plain-language farmer advice (English + Hindi).

Turns live weather + three simple farm answers (soil type, water, money) into short
sentences a farmer can read or listen to. The farmer never has to enter numbers.

The crop ranking still comes from the ML model (or the labelled baseline). This module
only (1) converts the farmer's simple answers into model inputs, (2) re-ranks by season,
water and budget, and (3) writes the result in words.
"""
from datetime import date, datetime
import requests

WEEKDAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEEKDAYS_HI = ["सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"]
WEEKDAYS_EN_SHORT = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WEEKDAYS_HI_SHORT = ["सोम", "मंगल", "बुध", "गुरु", "शुक्र", "शनि", "रवि"]

CROP_EN = {
    "rice": "Rice (Paddy)", "maize": "Maize (Corn)", "chickpea": "Chickpea (Chana)",
    "kidneybeans": "Kidney beans (Rajma)", "pigeonpeas": "Pigeon pea (Arhar/Tur)", "mothbeans": "Moth bean",
    "mungbean": "Green gram (Moong)", "blackgram": "Black gram (Urad)", "lentil": "Lentil (Masoor)",
    "pomegranate": "Pomegranate", "banana": "Banana", "mango": "Mango", "grapes": "Grapes",
    "watermelon": "Watermelon", "muskmelon": "Muskmelon", "apple": "Apple", "orange": "Orange",
    "papaya": "Papaya", "coconut": "Coconut", "cotton": "Cotton", "jute": "Jute", "coffee": "Coffee",
}
CROP_HI = {
    "rice": "धान", "maize": "मक्का", "chickpea": "चना", "kidneybeans": "राजमा", "pigeonpeas": "अरहर (तूर)",
    "mothbeans": "मोठ", "mungbean": "मूंग", "blackgram": "उड़द", "lentil": "मसूर", "pomegranate": "अनार",
    "banana": "केला", "mango": "आम", "grapes": "अंगूर", "watermelon": "तरबूज़", "muskmelon": "खरबूज़ा",
    "apple": "सेब", "orange": "संतरा", "papaya": "पपीता", "coconut": "नारियल", "cotton": "कपास",
    "jute": "जूट", "coffee": "कॉफ़ी",
}
CROP_EMOJI = {
    "rice": "🌾", "maize": "🌽", "chickpea": "🌱", "kidneybeans": "🌱", "pigeonpeas": "🌱", "mothbeans": "🌱",
    "mungbean": "🌱", "blackgram": "🌱", "lentil": "🌱", "pomegranate": "🌳", "banana": "🍌", "mango": "🥭",
    "grapes": "🍇", "watermelon": "🍉", "muskmelon": "🍈", "apple": "🍎", "orange": "🍊", "papaya": "🌳",
    "coconut": "🌴", "cotton": "☁️", "jute": "🌿", "coffee": "☕",
}

CROP_EN.update({
    "wheat": "Wheat (Gehun)", "mustard": "Mustard (Sarson)", "potato": "Potato (Aloo)", "onion": "Onion (Pyaz)",
    "tomato": "Tomato", "soybean": "Soybean", "groundnut": "Groundnut (Peanut)", "sorghum": "Sorghum (Jowar)",
    "pearlmillet": "Pearl millet (Bajra)", "okra": "Okra (Bhindi)",
})
CROP_HI.update({
    "wheat": "गेहूँ", "mustard": "सरसों", "potato": "आलू", "onion": "प्याज़", "tomato": "टमाटर",
    "soybean": "सोयाबीन", "groundnut": "मूंगफली", "sorghum": "ज्वार", "pearlmillet": "बाजरा", "okra": "भिंडी",
})
CROP_EMOJI.update({
    "wheat": "🌾", "mustard": "🌼", "potato": "🥔", "onion": "🧅", "tomato": "🍅", "soybean": "🌱",
    "groundnut": "🥜", "sorghum": "🌾", "pearlmillet": "🌾", "okra": "🌿",
})

# Crops missing from the public training dataset get a rule-based "climate fit" instead of an ML score.
# (ideal_temp_lo, ideal_temp_hi, ok_temp_lo, ok_temp_hi, ideal_rain_lo, ideal_rain_hi, ok_rain_lo, ok_rain_hi)
# Temperature = average of the next 7 days (deg C); rain = average monthly rain over the last ~3 months (mm).
# General agronomic ranges (assumption): confirm with local experts. If you later train on a dataset that
# contains one of these crops, the ML score is used for it automatically and this profile is ignored.
EXTRA_PROFILES = {
    "wheat": (12, 22, 5, 28, 10, 60, 0, 120),
    "mustard": (10, 25, 5, 30, 5, 50, 0, 100),
    "potato": (12, 24, 8, 28, 10, 70, 0, 150),
    "onion": (13, 28, 8, 33, 10, 80, 0, 150),
    "tomato": (18, 28, 12, 34, 20, 100, 0, 200),
    "soybean": (22, 30, 18, 34, 100, 250, 60, 400),
    "groundnut": (24, 32, 20, 36, 60, 200, 30, 300),
    "sorghum": (24, 32, 18, 38, 40, 180, 20, 300),
    "pearlmillet": (26, 34, 20, 40, 30, 150, 10, 250),
    "okra": (24, 32, 18, 38, 60, 200, 20, 350),
}


def _trap(v, lo, ilo, ihi, hi):
    if v < lo or v > hi: return 0.0
    if ilo <= v <= ihi: return 1.0
    return (v - lo) / (ilo - lo) if v < ilo else (hi - v) / (hi - ihi)


def climate_fit(prof, temperature, rain, irrigation):
    tlo_i, thi_i, tlo, thi, rlo_i, rhi_i, rlo, rhi = prof
    tf = _trap(temperature, tlo, tlo_i, thi_i, thi)
    rf = _trap(rain, rlo, rlo_i, rhi_i, rhi)
    if irrigation != "little":
        rf = max(rf, 0.6)  # a farmer who can irrigate is not limited by low rain
    return tf * rf


# Rough starting values for the model, chosen from the farmer's soil type.
# These are planning assumptions, NOT lab results: (N, P, K, pH).
SOILS = {
    "black": (50, 40, 100, 7.5),
    "red": (40, 30, 30, 6.0),
    "sandy": (30, 25, 30, 6.8),
    "loam": (80, 50, 50, 6.8),
    "clay": (70, 45, 60, 6.5),
    "unknown": (80, 50, 50, 6.8),
}
SOIL_NAME = {
    "black": ("black soil", "काली मिट्टी"), "red": ("red soil", "लाल मिट्टी"),
    "sandy": ("sandy soil", "रेतीली मिट्टी"), "loam": ("loamy soil", "दोमट मिट्टी"),
    "clay": ("clay soil", "चिकनी मिट्टी"), "unknown": ("land", "ज़मीन"),
}
# Budget the farmer can spend per acre (planning bands, matched to CROP_ECONOMICS in app.py).
BUDGET_PER_ACRE = {"low": 12000, "medium": 25000, "high": 50000}

# Widely taught soil-crop associations (planning assumption, not a lab result).
# 1.3 = grows well in this soil, 0.75 = usually a poor match.
SOIL_GOOD = {
    "black": {"cotton", "chickpea", "pigeonpeas", "orange", "grapes", "maize", "wheat", "soybean", "sorghum", "onion"},
    "red": {"pigeonpeas", "mothbeans", "mungbean", "blackgram", "mango", "pomegranate", "papaya", "groundnut", "sorghum", "tomato"},
    "sandy": {"watermelon", "muskmelon", "mothbeans", "pomegranate", "coconut", "mungbean", "groundnut", "pearlmillet"},
    "loam": {"maize", "lentil", "chickpea", "kidneybeans", "mungbean", "blackgram", "banana", "papaya", "orange", "apple", "wheat", "mustard", "potato", "onion", "tomato", "okra"},
    "clay": {"rice", "jute", "cotton", "banana", "lentil", "wheat"},
}
SOIL_POOR = {
    "black": {"coconut", "mothbeans"},
    "red": {"rice", "jute", "banana"},
    "sandy": {"rice", "jute", "banana", "chickpea", "lentil", "wheat"},
    "loam": set(),
    "clay": {"watermelon", "muskmelon", "mothbeans", "pomegranate", "groundnut", "potato"},
}


# Strongly regional crops (assumption, based on where they are mainly grown in India).
# The public crop dataset has no geography, so without this it could suggest apple in Rajasthan.
# (lat_min, lat_max, lon_min, lon_max)
REGIONS = {
    "jute": (20.0, 28.5, 85.0, 93.0),      # eastern India: West Bengal, Bihar, Assam, Odisha
    "coffee": (8.0, 15.5, 74.0, 78.7),     # Western Ghats hills: Karnataka, Kerala, Tamil Nadu
    "apple": (29.5, 37.5, 72.0, 97.5),     # Himalayan belt: J&K, Himachal, Uttarakhand, Arunachal
    # coconut: Kerala / Tamil Nadu / Karnataka, Konkan coast, and the east coast
    "coconut": [(6.0, 15.5, 74.0, 80.5), (15.0, 20.5, 72.5, 74.3), (13.0, 22.5, 79.5, 89.5)],
}


def region_factor(crop, lat, lon):
    boxes = REGIONS.get(crop)
    if boxes is None or lat is None or lon is None: return 1.0
    if isinstance(boxes, tuple): boxes = [boxes]
    return 1.0 if any(b[0] <= lat <= b[1] and b[2] <= lon <= b[3] for b in boxes) else 0.15


def soil_factor(soil, crop):
    if crop in SOIL_GOOD.get(soil, ()): return 1.3
    if crop in SOIL_POOR.get(soil, ()): return 0.75
    return 1.0


SEASON_NAME = {
    "Kharif": ("Kharif (rainy-season crops)", "खरीफ (बरसात की फसल)"),
    "Rabi": ("Rabi (winter crops)", "रबी (सर्दी की फसल)"),
    "Summer": ("Summer (zaid crops)", "गर्मी (जायद फसल)"),
}
DEFAULT_MONTHLY_RAIN = {"Kharif": 200, "Rabi": 40, "Summer": 40}

# weather_code -> (emoji, English, Hindi)
def wx(code):
    if code == 0: return ("☀️", "clear and sunny", "साफ़ धूप")
    if code in (1, 2): return ("🌤️", "mostly sunny", "ज़्यादातर धूप")
    if code == 3: return ("☁️", "cloudy", "बादल")
    if code in (45, 48): return ("🌫️", "foggy", "कोहरा")
    if code in (51, 53, 55, 56, 57): return ("🌦️", "light drizzle", "हल्की फुहार")
    if code in (61, 63, 65, 66, 67): return ("🌧️", "rainy", "बारिश")
    if code in (71, 73, 75, 77, 85, 86): return ("❄️", "snowy", "बर्फ़बारी")
    if code in (80, 81, 82): return ("🌦️", "rain showers", "बौछारें")
    if code in (95, 96, 99): return ("⛈️", "thunderstorm", "आंधी-बारिश")
    return ("🌤️", "changing weather", "बदलता मौसम")

TIP_TEXT = {
    "spray_hold": ("Do not spray medicine on crops – rain is likely and it will wash off.", "फसल पर दवा का छिड़काव न करें – बारिश हो सकती है और दवा बह जाएगी।"),
    "fert_hold": ("Wait before putting fertilizer – rain can wash it away.", "खाद डालना टाल दें – बारिश से खाद बह सकती है।"),
    "irrigation_skip": ("No need to water the field – rain is expected.", "खेत में पानी देने की ज़रूरत नहीं – बारिश की उम्मीद है।"),
    "spray_ok": ("Good time to spray – wind is low and no big rain.", "छिड़काव के लिए अच्छा समय – हवा कम है और बड़ी बारिश नहीं है।"),
    "wind_hold": ("Do not spray – strong wind will blow the medicine away.", "छिड़काव न करें – तेज़ हवा दवा उड़ा देगी।"),
    "irrigate_high_et": ("Land dries fast – water the field early morning or evening.", "ज़मीन जल्दी सूखती है – सुबह जल्दी या शाम को पानी दें।"),
    "drainage": ("Heavy rain – make sure water can flow out of the field.", "भारी बारिश – खेत से पानी निकलने का रास्ता साफ़ रखें।"),
    "heat": ("Very hot – protect young plants and water in cooler hours.", "बहुत गर्मी – छोटे पौधों को बचाएं और ठंडे समय में पानी दें।"),
    "cold": ("Very cold – protect young plants from frost.", "बहुत ठंड – छोटे पौधों को पाले से बचाएं।"),
}
TIP_ORDER = ["spray_hold", "irrigation_skip", "fert_hold", "drainage", "heat", "cold", "wind_hold", "irrigate_high_et", "spray_ok"]
TIP_ICON = {"go": "✅", "hold": "⏸️", "skip": "🚫", "warn": "⚠️"}


def current_season(d):
    m = d.month
    if 6 <= m <= 9: return "Kharif"
    if m in (10, 11, 12, 1, 2): return "Rabi"
    return "Summer"


def season_fit(crop_season, cur):
    parts = [p.strip() for p in crop_season.split("/")]
    if cur in parts: return 1.0
    if "Perennial" in parts: return 0.35
    if "Varies" in parts: return 0.35
    return 0.08


def water_factor(crop_water, have):
    if have == "little": return {"high": 0.25, "medium": 0.7}.get(crop_water, 1.0)
    if have == "some": return {"high": 0.6}.get(crop_water, 1.0)
    return 1.0


def join_list(items, lang):
    items = [i for i in items if i]
    if not items: return ""
    if len(items) == 1: return items[0]
    word = " and " if lang == "en" else " और "
    return ", ".join(items[:-1]) + word + items[-1]


def day_label(d, today, lang):
    delta = (d - today).days
    if delta == 0: return "Today" if lang == "en" else "आज"
    if delta == 1: return "Tomorrow" if lang == "en" else "कल"
    return (WEEKDAYS_EN if lang == "en" else WEEKDAYS_HI)[d.weekday()]


def _pd(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def _at(arr, i):
    arr = arr or []
    return arr[i] if i < len(arr) else None


def _mean(vals, default):
    v = [x for x in vals if x is not None]
    return sum(v) / len(v) if v else default


# ---------------- live data (Open-Meteo, no API key) ----------------
def fetch_forecast(lat, lon):
    params = {
        "latitude": lat, "longitude": lon, "timezone": "auto", "forecast_days": 7,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,et0_fao_evapotranspiration",
        "hourly": "relative_humidity_2m",
    }
    r = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=15)
    r.raise_for_status()
    return r.json()


def fetch_recent_rain_monthly(lat, lon):
    """Average monthly rain over the last ~3 months, or None if unavailable."""
    try:
        params = {"latitude": lat, "longitude": lon, "timezone": "auto", "past_days": 92,
                  "forecast_days": 1, "daily": "precipitation_sum"}
        r = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=15)
        r.raise_for_status()
        vals = [v for v in r.json().get("daily", {}).get("precipitation_sum", []) if v is not None]
        return sum(vals) / 3.0 if vals else None
    except Exception:
        return None


def reverse_place(lat, lon):
    """Best-effort village/town name for a GPS point (free BigDataCloud client endpoint)."""
    try:
        r = requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client",
                         params={"latitude": lat, "longitude": lon, "localityLanguage": "en"}, timeout=5)
        r.raise_for_status()
        j = r.json()
        return j.get("locality") or j.get("city") or j.get("principalSubdivision") or None
    except Exception:
        return None


# ---------------- the advice itself ----------------
def build_advice(econ_table, recommend_fn, calendar_fn, forecast, rain_monthly, place, soil, water, budget, lat=None, lon=None):
    daily = forecast.get("daily", {}) or {}
    days = daily.get("time", []) or []
    if not days:
        raise ValueError("no forecast")
    today = _pd(days[0])
    soil = soil if soil in SOILS else "unknown"
    water = water if water in ("plenty", "some", "little") else "some"
    budget = budget if budget in BUDGET_PER_ACRE else "medium"
    cur = current_season(today)

    # ---- turn live data + simple answers into model inputs ----
    tmax, tmin = daily.get("temperature_2m_max", []), daily.get("temperature_2m_min", [])
    temps = [(a + b) / 2 for a, b in zip(tmax, tmin) if a is not None and b is not None]
    temperature = min(55.0, max(0.0, _mean(temps, 25.0)))
    humidity = min(100.0, max(0.0, _mean((forecast.get("hourly", {}) or {}).get("relative_humidity_2m", []), 65.0)))
    rain = rain_monthly if rain_monthly is not None else DEFAULT_MONTHLY_RAIN[cur]
    rain = min(300.0, max(20.0, rain))
    n, p, k, ph = SOILS[soil]
    values = {"N": n, "P": p, "K": k, "temperature": temperature, "humidity": humidity, "ph": ph, "rainfall": rain}

    # Plenty of rain means a rain-only farmer is not really short of water.
    eff_water = {"little": "some", "some": "plenty"}.get(water, water) if rain >= 150 else water

    # ---- rank: model first, then season / water / budget ----
    recs = recommend_fn(values, 80)
    method = recs[0]["method"] if recs else "baseline"
    cands = []

    def add(key, e, base):
        fit = season_fit(e["season"], cur)
        cost_ratio = e["cost"] / BUDGET_PER_ACRE[budget]
        bf = 1.0 if cost_ratio <= 1 else (0.5 if cost_ratio <= 1.5 else 0.15)
        total = base * fit * water_factor(e["water"], eff_water) * bf * soil_factor(soil, key) * region_factor(key, lat, lon)
        cands.append((total, key, e, fit, cost_ratio))

    ml_keys = set()
    for r in recs:
        key = r["crop"].lower().replace(" ", "")
        ml_keys.add(key)
        e = econ_table.get(key)
        if e:
            add(key, e, (r["score"] if r["score"] is not None else 0) + 8)  # small floor so season can lift unlikely crops
    # crops the dataset does not contain: rule-based climate fit on a comparable scale
    for key, prof in EXTRA_PROFILES.items():
        e = econ_table.get(key)
        if e and key not in ml_keys:
            add(key, e, 8 + 45 * climate_fit(prof, temperature, rain, water))
    if not cands:
        raise ValueError("no crops")
    cands.sort(key=lambda c: c[0], reverse=True)
    top = cands[:5]
    _, bkey, be, bfit, bratio = top[0]

    # ---- this week in pictures ----
    week = []
    rainy = []
    for i, ds in enumerate(days):
        d = _pd(ds)
        emoji, _, _ = wx(_at(daily.get("weather_code"), i))
        pr = _at(daily.get("precipitation_probability_max"), i)
        ps = _at(daily.get("precipitation_sum"), i)
        is_rain = (pr is not None and pr >= 60) or (ps is not None and ps >= 5)
        if is_rain: rainy.append(d)
        week.append({"emoji": emoji, "rain": is_rain,
                     "day_en": WEEKDAYS_EN_SHORT[d.weekday()], "day_hi": WEEKDAYS_HI_SHORT[d.weekday()]})
    t_emoji, t_en, t_hi = wx(_at(daily.get("weather_code"), 0))
    avg_max = _mean(tmax, 28.0)
    if avg_max >= 38: tw = ("very hot weather", "बहुत गर्मी")
    elif avg_max >= 32: tw = ("hot weather", "गर्मी")
    elif avg_max >= 22: tw = ("pleasant weather", "सुहावना मौसम")
    elif avg_max >= 12: tw = ("cool weather", "हल्की ठंड")
    else: tw = ("cold weather", "कड़ाके की ठंड")

    # ---- weekly tips from the weather-adaptive calendar logic ----
    cal = calendar_fn(bkey, today, daily)
    grouped = {}
    for a in cal["forecast_advice"]:
        d = _pd(a["date"])
        for it in a["items"]:
            g = grouped.setdefault(it["key"], {"status": it["status"], "days": []})
            g["days"].append(d)
    tip_keys = [k_ for k_ in TIP_ORDER if k_ in grouped][:5]

    out = {}
    for lang in ("en", "hi"):
        i = 0 if lang == "en" else 1
        P = lambda en, hi: en if lang == "en" else hi

        crop_name = (CROP_EN if lang == "en" else CROP_HI).get(bkey, bkey)
        soil_name = SOIL_NAME[soil][i]
        season = SEASON_NAME[cur][i]
        greet = P("Namaste, farmer friend!", "नमस्ते किसान साथी!")
        place_phrase = "" if not place else P(f" near {place}", f" ({place} के पास)")
        soil_phrase = P(f"your {soil_name}", f"आपकी {soil_name}")
        p1 = P(f"{greet} Right now it is {season} season{place_phrase}. For {soil_phrase}, the best crop to grow is {crop_name}.",
               f"{greet} अभी {season} का मौसम है{place_phrase}। {soil_phrase} के लिए सबसे अच्छी फसल है {crop_name}।")

        # weather paragraph
        if rainy:
            labels = join_list([day_label(d, today, lang) for d in rainy], lang)
            rain_s = P(f"Rain is likely on {labels}.", f"{labels} को बारिश की संभावना है।")
        else:
            rain_s = P("No big rain is expected this week.", "इस हफ़्ते बड़ी बारिश की उम्मीद नहीं है।")
        p2 = P(f"Weather: today is {t_en}. This week: {tw[0]}. {rain_s}",
               f"मौसम: आज {t_hi} है। इस हफ़्ते: {tw[1]}। {rain_s}")

        # money / water / time
        if bratio <= 0.7: cost_ph = P("fits your budget easily", "आपके बजट में आराम से आ जाएगी")
        elif bratio <= 1.0: cost_ph = P("fits your budget", "आपके बजट में आ जाएगी")
        elif bratio <= 1.5: cost_ph = P("costs a little more than your budget", "आपके बजट से थोड़ी महंगी है")
        else: cost_ph = P("costs much more than your budget", "आपके बजट से बहुत महंगी है")
        ratio = (be["yield_t"] * be["price"] - be["cost"]) / be["cost"]
        if ratio >= 1.0: earn_ph = P("good earning is possible", "अच्छी कमाई की उम्मीद है")
        elif ratio >= 0.3: earn_ph = P("a fair earning is possible", "ठीक-ठाक कमाई की उम्मीद है")
        elif ratio >= 0: earn_ph = P("earning is likely to be small", "कमाई कम रह सकती है")
        else: earn_ph = P("it may not even cover the cost", "लागत भी निकलना मुश्किल हो सकता है")
        water_ph = {"high": P("needs a lot of water", "इसे बहुत पानी चाहिए"),
                    "medium": P("needs some water", "इसे थोड़ा पानी चाहिए"),
                    "low": P("needs very little water", "इसे बहुत कम पानी चाहिए")}[be["water"]]
        months = round(be["days"] / 30)
        if be["days"] >= 330:
            time_ph = P("a long-term crop – it takes more than a year to give fruit", "लंबी अवधि की फसल – फल आने में एक साल से ज़्यादा लगता है")
            time_s = P(f"It is {time_ph}.", f"यह {time_ph}।")
        else:
            time_ph = P(f"ready in about {months} months", f"लगभग {months} महीने में तैयार")
            time_s = P(f"It is {time_ph}.", f"यह {time_ph} हो जाती है।")
        warn_s = ""
        if be["water"] == "high" and eff_water == "little":
            warn_s = P(" Careful: this crop needs a lot of water and you have little.",
                       " ध्यान दें: इस फसल को ज़्यादा पानी चाहिए और आपके पास पानी कम है।")
        p3 = P(f"This crop {cost_ph}. At usual market prices, {earn_ph}. It {water_ph}. {time_s}{warn_s}",
               f"यह फसल {cost_ph}। आम बाज़ार भाव पर {earn_ph}। {water_ph}। {time_s}{warn_s}")

        # other options
        others = []
        for _, okey, oe, _, orat in top[1:]:
            oname = (CROP_EN if lang == "en" else CROP_HI).get(okey, okey)
            oratio = (oe["yield_t"] * oe["price"] - oe["cost"]) / oe["cost"]
            o_earn = (P("good earning possible", "अच्छी कमाई संभव") if oratio >= 1.0 else
                      P("fair earning possible", "ठीक-ठाक कमाई संभव") if oratio >= 0.3 else
                      P("small earning", "कमाई कम"))
            o_water = {"high": P("needs a lot of water", "ज़्यादा पानी चाहिए"),
                       "medium": P("needs some water", "थोड़ा पानी चाहिए"),
                       "low": P("needs little water", "कम पानी चाहिए")}[oe["water"]]
            others.append({"emoji": CROP_EMOJI.get(okey, "🌱"), "name": oname, "line": f"{o_earn}, {o_water}"})
        p4 = ""
        if others:
            names = join_list([o["name"] for o in others], lang)
            p4 = P(f"Other good choices: {names}.", f"दूसरे अच्छे विकल्प: {names}।")

        disclaimer = P(
            "This is general guidance. We guessed your soil richness from the soil type you chose, and prices and weather can change. "
            "Please also ask your local agriculture officer (KVK) before spending money.",
            "यह सामान्य सलाह है। हमने आपकी मिट्टी की ताक़त आपकी चुनी मिट्टी के प्रकार से अंदाज़े से ली है, और भाव व मौसम बदल सकते हैं। "
            "पैसा लगाने से पहले अपने स्थानीय कृषि अधिकारी (KVK) से भी ज़रूर पूछ लें।")

        # reasons for the best crop
        reasons = [P("Your soil type and the weather of your area suit it.", "आपकी मिट्टी और आपके इलाके का मौसम इसके लिए ठीक है।")]
        if bfit >= 1.0:
            reasons.insert(0, P("This is the right season for it.", "यह इसके लिए सही मौसम है।"))
        elif bfit >= 0.3:
            reasons.insert(0, P("It is a long-term tree crop, so plan for the coming years.", "यह लंबी अवधि की पेड़ वाली फसल है, आने वाले सालों की योजना बनाएं।"))
        else:
            reasons.insert(0, P("Note: this is not its usual season, so choose the sowing time carefully.", "ध्यान दें: यह इसका सामान्य मौसम नहीं है, इसलिए बुवाई का समय सोच-समझकर चुनें।"))
        sf = soil_factor(soil, bkey)
        if sf > 1: reasons.append(P(f"It grows well in {soil_name}.", f"यह {soil_name} में अच्छी उगती है।"))
        elif sf < 1: reasons.append(P(f"Note: it is not the easiest crop for {soil_name}.", f"ध्यान दें: {soil_name} में यह फसल थोड़ी मुश्किल हो सकती है।"))
        if rain >= 150 and be["water"] == "high":
            reasons.append(P("Recent rain is good for this crop.", "हाल की बारिश इस फसल के लिए अच्छी है।"))
        elif rain <= 60 and be["water"] == "low":
            reasons.append(P("It does well even with little rain.", "यह कम बारिश में भी अच्छी होती है।"))

        chips = [{"icon": "💰", "text": cost_ph}, {"icon": "💵", "text": earn_ph},
                 {"icon": "💧", "text": water_ph}, {"icon": "⏳", "text": time_ph}]

        # tips
        tips = []
        for key in tip_keys:
            g = grouped[key]
            if len(g["days"]) >= len(days):
                dtxt = P("All week", "पूरे हफ़्ते")
            else:
                dtxt = join_list([day_label(d, today, lang) for d in g["days"]], lang)
            tips.append({"icon": TIP_ICON.get(g["status"], "•"), "text": f"{dtxt}: {TIP_TEXT[key][i]}"})
        if not tips:
            tips.append({"icon": "✅", "text": P("Weather looks fine for normal farm work this week.", "इस हफ़्ते खेत के सामान्य काम के लिए मौसम ठीक है।")})

        paragraphs = [p1, p2, p3] + ([p4] if p4 else []) + [disclaimer]
        out[lang] = {
            "paragraphs": paragraphs,
            "best": {"emoji": CROP_EMOJI.get(bkey, "🌱"), "name": crop_name, "reasons": reasons, "chips": chips},
            "others": others, "tips": tips, "disclaimer": disclaimer,
            "speech": " ".join(paragraphs[:-1]),
        }
    return {"place": place, "week": week, "today_emoji": t_emoji, "method": method, "text": out}
