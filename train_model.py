"""Train and honestly evaluate crop-recommendation models from data/Crop_recommendation.csv.

Columns required: N,P,K,temperature,humidity,ph,rainfall,label  (every matching CSV in data/ is merged)
Steps: stratified 80/20 hold-out split (seed 42) -> compare several models by 5-fold CV on the
training part -> pick the best -> report hold-out accuracy next to a simple nearest-centroid
baseline -> save models/crop_model.joblib and models/metrics.json (shown by /api/health).

Environment overrides (used for testing): KM_DATA, KM_MODEL.
Note: the score measures agreement with this dataset's labels, NOT farm yield or profit.
"""
import json, os
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

BASE = Path(__file__).resolve().parent
DATA = Path(os.environ.get("KM_DATA", BASE / "data" / "Crop_recommendation.csv"))
OUT = Path(os.environ.get("KM_MODEL", BASE / "models" / "crop_model.joblib"))
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
TARGET = "label"

def main():
    # Every CSV in data/ that has the required columns is used, so "more data" = drop another file in.
    # (KM_DATA, used for testing, points at one single file instead.)
    files = [DATA] if os.environ.get("KM_DATA") else sorted(DATA.parent.glob("*.csv"))
    frames = []
    for f in files:
        if not f.exists():
            continue
        d = pd.read_csv(f)
        if all(c in d.columns for c in FEATURES + [TARGET]):
            frames.append(d[FEATURES + [TARGET]])
            print(f"Using {f.name}: {len(d)} rows")
        else:
            print(f"Skipping {f.name}: needs columns {FEATURES + [TARGET]}")
    if not frames:
        raise SystemExit("No dataset found. Run `python get_data.py` or save Crop_recommendation.csv into data/ (see README).")
    df = pd.concat(frames, ignore_index=True).dropna().drop_duplicates()
    X, y = df[FEATURES], df[TARGET].astype(str).str.lower().str.replace(" ", "")
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    candidates = {
        "RandomForest": RandomForestClassifier(n_estimators=300, min_samples_leaf=2, random_state=42, n_jobs=-1),
        "ExtraTrees": ExtraTreesClassifier(n_estimators=300, min_samples_leaf=2, random_state=42, n_jobs=-1),
        "KNN(scaled)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=7, weights="distance")),
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = {}
    for name, m in candidates.items():
        s = cross_val_score(m, X_tr, y_tr, cv=cv, scoring="accuracy", n_jobs=-1)
        cv_scores[name] = (float(s.mean()), float(s.std()))
        print(f"{name:14s} 5-fold CV (train part): {s.mean():.3f} ± {s.std():.3f}")
    best = max(cv_scores, key=lambda k: cv_scores[k][0])
    model = candidates[best].fit(X_tr, y_tr)

    pred = model.predict(X_te)
    acc = float(accuracy_score(y_te, pred))
    base = make_pipeline(StandardScaler(), NearestCentroid()).fit(X_tr, y_tr)
    base_acc = float(accuracy_score(y_te, base.predict(X_te)))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, OUT)
    metrics = {
        "model": best, "rows": int(len(df)), "train_rows": int(len(X_tr)), "test_rows": int(len(X_te)),
        "classes": sorted(set(y)), "holdout_accuracy": round(acc, 4),
        "cv_accuracy_mean": round(cv_scores[best][0], 4), "cv_accuracy_std": round(cv_scores[best][1], 4),
        "nearest_centroid_baseline_accuracy": round(base_acc, 4),
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": "Agreement with the dataset's own labels; not a measure of real farm yield or profit.",
    }
    (OUT.parent / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(f"\nRows: {len(df)} | train {len(X_tr)} | test {len(X_te)} | crops: {y.nunique()}")
    print(f"Chosen model: {best}")
    print(f"Held-out accuracy: {acc:.3f}   (simple nearest-centroid baseline: {base_acc:.3f})")
    print("\nPer-class report:\n", classification_report(y_te, pred, zero_division=0))
    print(f"Saved model to: {OUT}\nSaved metrics to: {OUT.parent / 'metrics.json'}")
    print("Important: this score measures agreement with this dataset's labels, not real-world yield or farm success.")

if __name__ == "__main__":
    main()
