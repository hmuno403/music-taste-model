"""
Music Taste Rating System
------------------------
Extracts audio features from a folder of songs and predicts a score (0-10)
based on user-defined taste pillars. Outputs a CSV with predictions and
placeholders for final scores.
"""

import os
import librosa
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression

# ------------------------------------------------------------
# SCORING WEIGHTS (calibrated to user's taste)
# ------------------------------------------------------------
WEIGHTS = {
    "base_score": 7.5,
    "tempo_bonus_slow_groove": 1,      # 70-100 BPM
    "tempo_penalty_very_slow": -1,     # < 70 BPM
    "centroid_warm": 1.5,              # spectral centroid < 900 Hz
    "centroid_harsh": -1,              # > 1200 Hz
    "loudness_penalty": -0.5,          # > -9 dB (over-compressed)
    "dynamic_sweet": 1.5,              # dynamic complexity 3-5
    "dynamic_low": -1,                 # < 2
    "evolution_bonus_high": 3,         # top 30% evolution
    "evolution_bonus_medium": 1,       # middle 40%
    "loop_penalty": -3,                # bottom 30% evolution
    "crescendo_bonus": 3,              # RMS slope > 1.5 dB/min
    "dance_energy_bonus": 1.5,         # tempo > 120 + top 30% evolution
}

def get_crescendo_slope(y, sr):
    """Estimate how much the loudness increases over the song (dB per minute)."""
    n_segments = 10
    seg_len = len(y) // n_segments
    rms_vals = []
    for i in range(n_segments):
        seg = y[i*seg_len : (i+1)*seg_len]
        rms = np.sqrt(np.mean(seg**2))
        rms_db = 20 * np.log10(rms + 1e-9)
        rms_vals.append(rms_db)
    X = np.arange(n_segments).reshape(-1, 1)
    model = LinearRegression().fit(X, rms_vals)
    slope = model.coef_[0]  # dB per segment
    duration_min = (len(y) / sr) / 60
    if duration_min > 0:
        slope_per_min = slope * (n_segments / duration_min)
    else:
        slope_per_min = 0
    return slope_per_min

def get_features(filepath, duration=120):
    """Extract audio features from the first `duration` seconds."""
    y, sr = librosa.load(filepath, duration=duration)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    tempo = tempo if not isinstance(tempo, np.ndarray) else tempo[0]
    rms = librosa.feature.rms(y=y)[0]
    loudness_db = 20 * np.log10(rms.mean() + 1e-9)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0].mean()
    rms_db = 20 * np.log10(rms + 1e-9)
    dynamic_complexity = np.std(rms_db)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    evolution = np.std(onset_env)
    crescendo_slope = get_crescendo_slope(y, sr)
    return {
        "tempo": tempo,
        "loudness_db": loudness_db,
        "spectral_centroid": centroid,
        "dynamic_complexity": dynamic_complexity,
        "evolution": evolution,
        "crescendo_slope": crescendo_slope,
    }

def predict_score(features):
    """Apply the rule‑based scoring model to a feature dictionary."""
    score = WEIGHTS["base_score"]
    if 70 <= features["tempo"] <= 100:
        score += WEIGHTS["tempo_bonus_slow_groove"]
    elif features["tempo"] < 70:
        score += WEIGHTS["tempo_penalty_very_slow"]
    if features["spectral_centroid"] < 900:
        score += WEIGHTS["centroid_warm"]
    elif features["spectral_centroid"] > 1200:
        score += WEIGHTS["centroid_harsh"]
    if features["loudness_db"] > -9:
        score += WEIGHTS["loudness_penalty"]
    dc = features["dynamic_complexity"]
    if dc < 2:
        score += WEIGHTS["dynamic_low"]
    elif 3 <= dc <= 5:
        score += WEIGHTS["dynamic_sweet"]
    if features["crescendo_slope"] > 1.5:
        score += WEIGHTS["crescendo_bonus"]
    return score

def main():
    folder = input("Enter the path to the folder containing audio files: ").strip()
    folder = os.path.expanduser(folder)
    if not os.path.isdir(folder):
        print("Folder not found.")
        return

    audio_files = list(Path(folder).glob("*.flac")) + list(Path(folder).glob("*.mp3")) + list(Path(folder).glob("*.wav"))
    if not audio_files:
        print("No .flac, .mp3, or .wav files found.")
        return

    print(f"Found {len(audio_files)} files. Analyzing...")
    results = []
    evolution_values = []

    for f in audio_files:
        print(f"  Processing {f.name}...")
        try:
            feats = get_features(str(f))
            feats["filename"] = f.name
            results.append(feats)
            evolution_values.append(feats["evolution"])
        except Exception as e:
            print(f"    ERROR: {e}")

    if not results:
        return

    ev_arr = np.array(evolution_values)
    ev_high = np.percentile(ev_arr, 70)
    ev_low = np.percentile(ev_arr, 30)

    final_rows = []
    for feats in results:
        ev = feats["evolution"]
        if ev >= ev_high:
            ev_bonus = WEIGHTS["evolution_bonus_high"]
            high_evo = True
        elif ev <= ev_low:
            ev_bonus = WEIGHTS["loop_penalty"]
            high_evo = False
        else:
            ev_bonus = WEIGHTS["evolution_bonus_medium"]
            high_evo = False

        score = predict_score(feats) + ev_bonus
        if feats["tempo"] > 120 and high_evo:
            score += WEIGHTS["dance_energy_bonus"]

        score = max(0, min(10, round(score, 1)))

        row = {
            "filename": feats["filename"],
            "predicted_score": score,
            "final_score": "",
            "tempo": round(feats["tempo"], 1),
            "loudness_db": round(feats["loudness_db"], 1),
            "spectral_centroid": round(feats["spectral_centroid"], 1),
            "dynamic_complexity": round(feats["dynamic_complexity"], 2),
            "evolution": round(feats["evolution"], 3),
            "crescendo_slope": round(feats["crescendo_slope"], 2),
        }
        final_rows.append(row)

    df = pd.DataFrame(final_rows)
    out_csv = os.path.join(folder, "predicted_ratings.csv")
    df.to_csv(out_csv, index=False)
    print(f"\n✅ Predictions saved to: {out_csv}")
    print("\nFirst 10 predictions:")
    print(df[["filename", "predicted_score"]].head(10))

if __name__ == "__main__":
    main()