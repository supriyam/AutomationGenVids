# 🎬 YouTube Faceless Video Automation (Gemini Edition)

Fully automated pipeline: **Topic → Script → Images → Voiceover → MP4 Video**
Powered by **Google Gemini Pro** (script) + **ElevenLabs** (voice) + **MoviePy** (video)

---

## 📁 Project Structure

```
youtube_automation/
├── main.py                  ← Entry point — run this
├── requirements.txt         ← Python dependencies
├── .env.example             ← Rename to .env and add your keys
├── src/
│   ├── config.py            ← All settings (model, niche, video size)
│   ├── pipeline.py          ← Orchestrates all 4 steps
│   ├── script_generator.py  ← Gemini generates script + image prompts
│   ├── image_handler.py     ← Saves prompts + creates placeholder images
│   ├── voiceover.py         ← ElevenLabs generates MP3 per scene
│   └── video_assembler.py   ← MoviePy assembles final MP4
└── output/
    └── {timestamp}/         ← Each run gets its own folder
        ├── script.json
        ├── image_prompts.txt
        ├── images/
        ├── audio/
        └── video/
```

---

## ⚙️ Setup (One-Time)

### 1. Install Python 3.10+
Download from https://python.org if you don't have it.

### 2. Open folder in VS Code
`File → Open Folder → select youtube_automation/`

### 3. Open VS Code Terminal
`View → Terminal`  (or Ctrl + `)

### 4. Create & activate a virtual environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 5. Install dependencies
```bash
pip install -r requirements.txt
```

### 6. Install ffmpeg (required for video/audio)
- **Windows:** https://ffmpeg.org/download.html → add to PATH
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

### 7. Add your API keys
```bash
cp .env.example .env   # Mac/Linux
copy .env.example .env # Windows
```
Open `.env` and fill in:

| Key | Where to get it | Cost |
|---|---|---|
| `GEMINI_API_KEY` | https://aistudio.google.com/app/apikey | Free (1500 req/day) |
| `ELEVENLABS_API_KEY` | https://elevenlabs.io/app/settings/api-keys | Free (10k chars/mo) |

---

## 🚀 Running the Pipeline

### Option A — Interactive prompt
```bash
python main.py
```

### Option B — Pass topic directly
```bash
python main.py 5 AI tools that replace expensive software in 2025
```

---

## 🤖 Changing the Gemini Model

Edit `src/config.py`:

```python
GEMINI_MODEL: str = "gemini-2.0-flash"   # default — fast & free
# GEMINI_MODEL: str = "gemini-1.5-pro"   # higher quality
# GEMINI_MODEL: str = "gemini-2.5-pro"   # best quality
```

---

## ⚙️ Other Customization (src/config.py)

| Setting | Default | Description |
|---|---|---|
| `NICHE` | `"AI Tools"` | Your YouTube channel niche |
| `SCENES_COUNT` | `5` | Scenes per video |
| `VIDEO_WIDTH/HEIGHT` | `1920×1080` | Output resolution |
| `ELEVENLABS_VOICE_ID` | Rachel | Change to any ElevenLabs voice |

---

## 🖼️ Replacing Placeholder Images

1. Open `output/{timestamp}/image_prompts.txt`
2. Copy each scene prompt → paste into **Leonardo.ai** or **Ideogram.ai**
3. Download images → replace `output/{timestamp}/images/scene_0X.png`
4. Re-run the script on the same topic to re-render video with new images

---

## 📤 What You Get Per Run

| File | Description |
|---|---|
| `script.json` | Full structured script from Gemini |
| `image_prompts.txt` | Copy-paste prompts for any image AI |
| `images/scene_XX.png` | Placeholder images (replace with real ones) |
| `audio/scene_XX.mp3` | Per-scene ElevenLabs voiceover |
| `audio/full_voiceover.mp3` | Combined audio track |
| `video/YourTitle.mp4` | 🎬 Final YouTube-ready MP4 |

---

## ❓ Troubleshooting

| Error | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` with venv active |
| `ffmpeg not found` | Install ffmpeg and add to PATH |
| `Gemini 403 / invalid key` | Check GEMINI_API_KEY in `.env` |
| `ElevenLabs 401` | Check ELEVENLABS_API_KEY in `.env` |
| `JSON decode error` | Gemini returned bad JSON — just run again |
