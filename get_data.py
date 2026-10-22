"""Download the public Crop Recommendation dataset to data/Crop_recommendation.csv.

Run:  python get_data.py            (tries a few public mirrors)
      python get_data.py --url <direct-csv-link>

If every mirror fails (no internet, or a mirror moved), download the CSV by hand from
https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
and save it as data/Crop_recommendation.csv. Then run: python train_model.py
"""
import io, sys
from pathlib import Path
import requests

OUT = Path(__file__).resolve().parent / "data" / "Crop_recommendation.csv"
COLS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "label"]
MIRRORS = [  # public GitHub copies of the same Kaggle file; any one working is enough
    "https://raw.githubusercontent.com/Gladiator07/Harvestify/master/Data-processed/crop_recommendation.csv",
    "https://raw.githubusercontent.com/DataWithVishal/CropRecommendation/main/Crop_recommendation.csv",
    "https://raw.githubusercontent.com/dsrscientist/dataset1/master/Crop_recommendation.csv",
]

def valid(text):
    import pandas as pd
    try:
        df = pd.read_csv(io.StringIO(text))
    except Exception:
        return False
    return all(c in df.columns for c in COLS) and len(df) > 1000 and df["label"].nunique() >= 15

def main():
    if OUT.exists() and valid(OUT.read_text(encoding="utf-8", errors="ignore")):
        print(f"Dataset already present: {OUT}")
        return 0
    urls = [sys.argv[2]] if len(sys.argv) > 2 and sys.argv[1] == "--url" else MIRRORS
    for u in urls:
        try:
            r = requests.get(u, timeout=30)
            if r.status_code == 200 and valid(r.text):
                OUT.parent.mkdir(parents=True, exist_ok=True)
                OUT.write_text(r.text, encoding="utf-8")
                print(f"Downloaded dataset from {u}\nSaved to {OUT}")
                return 0
            print(f"Skipped {u} (HTTP {r.status_code} or unexpected content)")
        except requests.RequestException as e:
            print(f"Could not reach {u}: {e.__class__.__name__}")
    print("\nCould not download the dataset automatically.\n"
          "Download Crop_recommendation.csv from the Kaggle page in the header of this file\n"
          f"and save it as {OUT}, then run: python train_model.py")
    return 1

if __name__ == "__main__":
    sys.exit(main())
