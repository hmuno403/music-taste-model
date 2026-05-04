# Music Taste Rating System

I built this because streaming recommendations never understood why I love a repetitive Lana Del Rey track but can't stand a cheesy Lizzo anthem. These seven pillars are my actual taste, reverse‑engineered from years of rating songs.

## 🎧 The Seven Pillars (my rules for a good song)

1. **Controlled escalation** – songs must build (soft→loud, sparse→dense)
2. **Earned theatricality** – drama is great if genuine; no over‑acting
3. **Warm organic production** – clear, warm mixes preferred
4. **Repetition that evolves** – loops are fine if something changes
5. **Atmospheric / spoken word** – vulnerable delivery can score high without a build
6. **Anti‑cheese filter** – reject forced anthems, performative empowerment
7. **Intentional weirdness** – cold/glitchy production allowed if artistic (Crystal Castles, Grimes)

## 🛠 How It Works

The script extracts audio features using `librosa` (tempo, loudness, spectral centroid, dynamic complexity, evolution, crescendo slope). Then it applies a rule‑based scoring model I calibrated on hundreds of my own long‑term ratings.

Output is a CSV with predicted scores (0‑10) and a blank `final_score` column – you listen, you rate, the model learns (eventually).

**Current accuracy**: ~70%. The rest needs lyrics, vibe, and a human ear.

## 📦 Installation

    git clone https://github.com/hmuno403/music-taste-model.git
    cd music-taste-model
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt

**Requires `ffmpeg`** for MP3 decoding:  
- macOS: `brew install ffmpeg`  
- Ubuntu: `sudo apt install ffmpeg`

## 🏃 Usage

1. Put your audio files (`.flac`, `.mp3`, `.wav`) in a folder.
2. Run: `python rate_audio.py`
3. Enter the folder path when prompted.
4. Open the generated `predicted_ratings.csv`.
5. Listen to tracks with predicted score ≥ 7, then fill in your actual `final_score`.

## 🍎 Integration with Apple Music (optional)

After you have the CSV, you can add the scores to your Apple Music library:

- Add the album to your library.
- Edit the **Comments** field for each track (right‑click → Get Info → Comments).
- Paste the predicted score (e.g., `9.5`).
- Create **Smart Playlists** that filter by comment (e.g., “Comment contains 9”).
- Later, update the comment with your final score.

This turns the script into a living rating system that grows with you.

## 📈 Example Output (real examples from my listening)

| filename | predicted_score | final_score | tempo | loudness_db |
|----------|----------------|-------------|-------|--------------|
| Bowling alley.flac | 10.0 | | 95.1 | -9.3 |
| Thirst Trap.flac | 10.0 | | 119.0 | -8.0 |
| Some Girls.flac | 8.5 | | 129.8 | -7.3 |

## 🔍 Limitations

- **70% accuracy** – doesn't capture lyrics, authenticity, or cultural context.
- Best used as a filter: predicted ≥ 7 → “likely worth listening”.
- No artist‑specific offsets; purely acoustic.

## 🧠 What I learned

Audio features get you about 70% of the way. The rest is lyrics, vibe, and whether a song tries too hard. This script helped me curate my yearly playlists – and taught me that my taste is more consistent than I thought.

## 📄 License

MIT