"""
config.py — All settings and API keys for the pipeline.
Edit this file before running.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ─────────────────────────────────────────────
    # 🔑 API KEYS — set in .env or paste directly
    # ─────────────────────────────────────────────
    GEMINI_API_KEY: str     = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "YOUR_ELEVENLABS_API_KEY")

    # ─────────────────────────────────────────────
    # 🤖 Gemini Settings
    # ─────────────────────────────────────────────
    # Options: gemini-2.0-flash (fastest/free) | gemini-1.5-pro | gemini-2.5-pro
    GEMINI_MODEL: str = "gemini-2.0-flash"
    MAX_TOKENS: int   = 2000

    # ─────────────────────────────────────────────
    # 🎙️ ElevenLabs Voice Settings
    # ─────────────────────────────────────────────
    # Find voice IDs at: https://elevenlabs.io/voice-library
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Default: Rachel
    ELEVENLABS_MODEL: str    = "eleven_monolingual_v1"
    VOICE_STABILITY: float   = 0.5
    VOICE_SIMILARITY: float  = 0.75

    # ─────────────────────────────────────────────
    # 📺 Video Settings
    # ─────────────────────────────────────────────
    NICHE: str              = "AI Tools"      # Change to your niche
    SCENES_COUNT: int       = 5               # Number of scenes
    VIDEO_WIDTH: int        = 1920
    VIDEO_HEIGHT: int       = 1080
    FPS: int                = 24
    SCENE_DURATION: int     = 5               # Seconds per scene (when no audio)
    FONT_SIZE: int          = 48
    SUBTITLE_FONT_SIZE: int = 36
    BACKGROUND_COLOR: str   = "#0a0a0a"       # Dark background for placeholder images

    # ─────────────────────────────────────────────
    # 📁 Output Paths
    # ─────────────────────────────────────────────
    OUTPUT_DIR: str    = "./output"
    SCRIPTS_DIR: str   = "./output/scripts"
    IMAGES_DIR: str    = "./output/images"
    AUDIO_DIR: str     = "./output/audio"
    VIDEOS_DIR: str    = "./output/videos"

config = Config()
