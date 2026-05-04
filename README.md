# Music Taste Rating System

A hybrid music scoring system that predicts how much a user will like a song based on **audio features + qualitative taste pillars**.

## 🎧 The Seven Pillars

1. **Controlled escalation** – songs must build (soft→loud, sparse→dense)
2. **Earned theatricality** – drama is great if genuine; no over‑acting
3. **Warm organic production** – clear, warm mixes preferred
4. **Repetition that evolves** – loops are fine if something changes
5. **Atmospheric / spoken word** – vulnerable delivery can score high without a build
6. **Anti‑cheese filter** – reject forced anthems, performative empowerment
7. **Intentional weirdness** – cold/glitchy production allowed if artistic

## 🛠 How It Works

1. Extracts audio features using `librosa` (tempo, loudness, spectral centroid, dynamic complexity, evolution, crescendo slope)
2. Applies a rule‑based scoring model calibrated on long‑term listening data
3. Outputs a CSV with predicted scores (0‑10) and a blank `final_score` column for listening validation
4. Achieves ~70% accuracy; lyrics and cultural context needed for the remaining 30%

## 📦 Installation

    git clone https://github.com/hmuno403/music-taste-model.git
    cd music-taste-model
    python -m venv venv
    source venv/bin/activate   # or venv\Scripts\activate on Windows
    pip install -r requirements.txt

> **Requires `ffmpeg`** for MP3 decoding. Install it:
> - macOS: `brew install ffmpeg`
> - Ubuntu: `sudo apt install ffmpeg`

## 🏃 Usage

Place your audio files (`.flac`, `.mp3`, `.wav`) in a folder, then run:

    python rate_audio.py

Enter the folder path when prompted. The script generates `predicted_ratings.csv` inside that folder.

Open the CSV, listen to tracks with predicted score ≥ 7, and fill in your actual `final_score` over time.

### Integration with Apple Music (optional)

After generating `predicted_ratings.csv`, you can use the scores to organise your Apple Music library:

1. **Add the album** to your Apple Music library.
2. **Edit the Comments field** for each track:
   - Select tracks → right‑click → **Get Info** → **Comments** tab.
   - Paste the predicted score (e.g., `9.5`).
3. **Create Smart Playlists** to automatically group songs by score:
   - File → New → Smart Playlist.
   - Rule: `Comments` `contains` `9` (for all tracks rated 9+).
4. **Update comments later** with your final score after listening.

> 💡 This turns the script into a living rating system integrated with your daily listening.

## 📈 Example Output

| filename | predicted_score | final_score | tempo | loudness_db |
|----------|----------------|-------------|-------|--------------|
| song1.flac | 9.5 | | 122.3 | -8.1 |
| song2.flac | 4.0 | | 65.2 | -10.5 |

## 🔍 Limitations

- **70% accuracy** – does not capture lyrics, authenticity, or cultural context.
- Best used as a filter: predicted ≥ 7 → “likely worth listening”.
- No artist‑specific offsets; purely acoustic.

## 📄 License

MIT