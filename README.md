# KisanMitra AI — Hackathon Prototype

A Flask web app for weather-aware farming decisions with a bilingual English/Hindi interface, live weather forecast, crop ranking, illustrative farm economics, and weather-triggered action suggestions.

## Two screens

- **`/` – Farmer screen (default).** Built for farmers who do not read charts or numbers. The farmer taps "Use my location" (or types a village/town), taps three big picture buttons (soil, water, money) and gets short advice in plain **Hindi or English**, with a "Listen" button that reads it aloud. No numbers to type, no statistics shown. Live weather and the last ~3 months of rainfall are fetched automatically from the location. It shows the best crop plus **four other options** from 32 crops, a **chat box** (type or speak any farming question) and the **Kisan Call Centre helpline 1800-180-1551** at the bottom. Advice covers: best crop now, two other choices, the week's weather in pictures, and what to do on the farm this week (spray, irrigate, fertilizer, drainage, heat/cold).
- **`/expert` – Detailed screen.** The numeric view with charts, the what-if simulator and the farming calendar, for officers and judges.

How the farmer screen works (`advice.py`, `POST /api/advice`): soil type is converted to rough starting soil values, the weather and rain come from Open-Meteo, the crop model ranks crops, and the ranking is then adjusted for the **current season**, the farmer's **water** and **budget**. The result is written as sentences from fixed templates (it is not a free-form chatbot). Soil richness is a guess from the soil type, and money words (cheap / fair earning) come from the illustrative cost and price placeholders below, so keep the "ask your KVK officer" note.

Location needs HTTPS (Render provides it) or `localhost`. If permission is denied, the farmer can type the place instead.

## What works

- Location search using Open-Meteo geocoding; no API key needed for typical non-commercial demo use.
- Current conditions plus a 7-day forecast: temperature, feels-like temperature, humidity, rain, wind, cloud cover, pressure, sunrise/sunset, UV, daily highs/lows and precipitation probability.
- Crop recommendation inputs: N, P, K, pH, temperature, humidity and estimated seasonal rainfall.
- Random Forest training/evaluation script, if you add the public crop dataset.
- Transparent baseline rankings work before the model is trained, and the UI explicitly labels this as a demo baseline.
- Farm budget/cost/revenue comparisons and weather-aware checks.
- Full static UI text toggles between English and Hindi; language choice persists in the browser.
- **What-if simulator** (`/api/crops` + client-side maths): compare crops and stress-test market price, input cost and yield (weather loss/gain) with sliders.
- **Weather-adaptive farming calendar** (`/api/calendar`): a crop-stage timeline from the sowing date plus forecast-adjusted actions for the next 7 days (hold spraying before rain, skip irrigation, irrigate early on high-evaporation days, heat/cold/drainage warnings). Re-searching the weather re-checks the plan and reports if it changed.
- Weather alerts and generated advice are translated on the client, so toggling Hindi updates them too.

## Windows setup (VS Code / PowerShell)

1. Install Python 3.10+ (3.11 recommended) and open this folder in VS Code.
2. Open Terminal → New Terminal.
3. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `.\.venv\Scripts\activate.bat` from Command Prompt instead.

4. Install libraries:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   python app.py
   ```

6. Open http://127.0.0.1:5000. Keep the terminal open while demonstrating.

Internet is required for weather lookup and the external fonts/chart library. The core page and recommendation fallback can still open if weather fails, but weather charts/cards need network access.

## Train the ML model (one step)

The project does not ship a trained model, and it never fakes one. Until you train it, the app uses a clearly labelled baseline ranking (the expert page badge says "Baseline demo").

```powershell
python get_data.py      # downloads the public Crop_recommendation.csv into data/
python train_model.py   # trains, evaluates, saves models/crop_model.joblib + models/metrics.json
```

If `get_data.py` cannot download it, get the file by hand from https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset and save it as `data/Crop_recommendation.csv`, then run `python train_model.py`. Restart `python app.py`; the badge changes to "Trained ML model active" and `/api/health` shows the metrics.

What `train_model.py` does: stratified 80/20 hold-out split (seed 42), compares RandomForest, ExtraTrees and a scaled KNN by 5-fold cross-validation on the training part, keeps the best, and reports the hold-out accuracy **next to a simple nearest-centroid baseline**, so you can show the ML adds value. Report only the numbers your own run prints.

**On Render** the build command runs both steps, so the deployed app is trained automatically (if the download fails, the build still succeeds and the baseline is used).

**Honest limits to mention in your pitch**
- The dataset is a balanced educational set of crop-condition examples. High accuracy means it agrees with the dataset's labels, not that a farm will earn money.
- It has 22 crops and **no wheat, mustard, soybean, groundnut, sorghum or sugarcane**, so in the Rabi season the suggestions are limited. A larger dataset would be the next step.

## How the farmer screen decides (what is ML and what is a rule)

1. **ML / baseline:** live temperature, humidity and recent rainfall (from the location) plus rough soil values (from the soil type) go into the crop model, which scores all 22 crops.
2. **Rules on top (assumptions, written in `advice.py`):** season fit (Kharif/Rabi/Summer from today's date), the farmer's water and budget, rain (plenty of rain means a rain-only farmer is not short of water), soil-crop matches (e.g. clay suits rice/jute, sandy suits melons), and four strongly regional crops (jute, coffee, apple, coconut) are only suggested where they are grown. These are general agronomic rules of thumb, not trained from data; confirm with local experts before relying on them.


## Chat box (ChatGPT-style)

The farmer screen has a chat card where the farmer can type or speak (🎤) any farming question and get a short answer in simple Hindi or English, with a 🔊 button to hear it. It uses the Claude API **from the server**, so the key stays secret. It also receives the app's own advice (place, weather, crop) so answers match what the farmer just saw.

- **Turn it on:** set an environment variable `ANTHROPIC_API_KEY` (locally: `$env:ANTHROPIC_API_KEY="sk-ant-..."` in PowerShell before `python app.py`; on Render: Environment tab). Without a key the chat card is simply hidden and everything else works.
- **Cost / safety:** each question is a paid API call. The app limits each visitor to 20 questions per 10 minutes and 300 per hour overall (`KM_CHAT_HOURLY_CAP`). Default model is `claude-haiku-5-5` (change with `KM_CHAT_MODEL`).
- **Safe behaviour (set in `chat.py`):** simple language, no exact pesticide doses, no invented prices or subsidy details, points to the Kisan Call Centre / KVK for serious problems and to 108 for emergencies. Still an AI: it can be wrong, so keep the "confirm with an expert" message in your pitch.

## More crops and more data

- The public dataset only knows **22 crops** (no wheat, mustard, potato, onion, tomato, soybean, groundnut, jowar, bajra, okra). The farmer screen adds these **10 with rule-based climate profiles** (`EXTRA_PROFILES` in `advice.py`) - general agronomic temperature and rain ranges, **not ML**. Say this in your pitch.
- If you train on a dataset that includes any of those crops, the ML score is used for them automatically.
- **More training data:** put any extra CSV with the columns `N,P,K,temperature,humidity,ph,rainfall,label` into `data/` and run `python train_model.py` again. All matching files are merged. Training the same file more times will not add crops or change results.
- **Helpline:** Kisan Call Centre **1800-180-1551**, toll-free, 6 am - 10 pm, all days, 22 languages (source: mkisan.gov.in/Home/AboutKCC).

## Budget estimates — read before presenting

The prototype includes per-acre assumptions in `app.py` for cost, yield and selling price so the budget comparison can be demonstrated immediately. They are **illustrative placeholders**, not current official district rates. The figures are scaled by the entered acreage; net = estimated gross revenue − estimated cultivation cost. They do not account for all possible labour, storage, transport, financing, weather loss, market variation or land rent.

For a credible local pilot, replace these values with current data from the relevant State Agriculture Department / Krishi Vigyan Kendra (KVK), MSP/mandi price sources where applicable, and record source/date/unit in the interface. Never present these estimates as guaranteed profit.

## Weather data

Uses Open-Meteo:
- Geocoding: `https://geocoding-api.open-meteo.com/v1/search`
- Forecast: `https://api.open-meteo.com/v1/forecast`

See https://open-meteo.com/en/docs and follow the current usage/licensing terms for your deployment. The dashboard displays the source. Forecast values are model forecasts, not ground-truth observations.

## Team split (2–4 people)

- Person 1: Flask/API, error handling, ML training and metrics.
- Person 2: UI styling, responsive layout, English/Hindi translations.
- Person 3: validate crop inputs, replace economic placeholders with sourced local values, prepare demo scenarios.
- Person 4 (if available): test location/API failures, prepare pitch, screenshots and deployment.

## 48-hour plan

**Hours 0–6:** install/run app, test weather search, review form and mobile layout.  
**Hours 6–16:** download dataset, train model, record actual held-out metrics; verify inputs.  
**Hours 16–26:** source local budget assumptions and label every assumption; refine bilingual text.  
**Hours 26–36:** test at least three scenarios (rain likely, limited budget, limited irrigation), test bad location and offline errors.  
**Hours 36–48:** rehearse a 3-minute demo, capture screenshots, prepare pitch and keep a working local fallback.

## Suggested live demo

1. Search a town or district and show current weather plus the 7-day forecast.
2. Enter soil-test values, land area, budget and irrigation availability.
3. Show top crop rankings, the model status and the explanation/limitations.
4. Change budget or irrigation and compare how the cost-fit indicator changes.
5. Toggle Hindi and show that labels and generated recommendations update.
6. Explain which estimates are placeholders and how they would be replaced with local verified data.


## Deploy to Render

The repository includes `render.yaml` and `gunicorn` for production deployment.

### Deploy from GitHub

1. Push the complete project folder to a GitHub repository. Keep `app.py`, `requirements.txt`, and `render.yaml` at the repository root.
2. Sign in to https://render.com and connect your GitHub account.
3. In the Render dashboard, choose **New → Blueprint** and select the KisanMitra AI repository.
4. Render should detect `render.yaml`. Review the service settings and create the web service.
5. Wait for the build and deployment to finish. Open the `onrender.com` URL Render gives you.
6. Check `<your-render-url>/api/health`; it should return JSON with `"status":"ok"`.

### If you prefer creating a Web Service manually

- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app --workers 2 --threads 4 --timeout 120`
- Health check path: `/api/health`

### Deployment notes

- Render free services may spin down after inactivity and take a little while to wake up.
- Weather is fetched server-side from Open-Meteo; no weather API key is configured or required for the typical demo.
- Do not use Flask's `app.run(debug=True)` as the production server. Render runs the app with Gunicorn.
- The trained model file under `models/` is ignored by Git. If you train a model, either commit the small `models/crop_model.joblib` file to your private/public repo if licensing and size allow, or use persistent/object storage and adjust loading. The app will still run without it, using the clearly labelled baseline ranking.
- Free instances have limited memory/CPU. If startup or model inference is slow, reduce worker count to `--workers 1 --threads 4`.
- Before public launch, replace illustrative crop economics with verified local data and clearly retain the estimate disclaimer.

## Project structure

```text
KisanMitra_AI/
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
├── data/
├── models/
├── templates/index.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## Safety and limitations

This is a hackathon decision-support prototype, not professional agronomic advice. Use soil-test data when possible and confirm crop choices, chemical use, irrigation, and financial decisions with local agricultural experts.
