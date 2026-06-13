"""
script_generator.py — Uses Google Gemini Pro to generate full video script
with scene breakdowns and image prompts.
"""

import json
import re
import requests
from src.config import config


SYSTEM_PROMPT = """You are a YouTube scriptwriter for faceless channels.
Output ONLY valid JSON — no markdown, no backticks, no extra text whatsoever.
Use this exact structure:
{
  "video_title": "Best SEO-optimized title",
  "hook": "Opening line to grab attention in first 3 seconds",
  "target_audience": "Who this is for",
  "estimated_duration": "X-Y minutes",
  "scenes": [
    {
      "number": 1,
      "title": "Scene title",
      "voiceover": "Full voiceover script for this scene. 3-5 sentences. Conversational and engaging.",
      "image_prompt": "Highly detailed image generation prompt. Include: style (photorealistic/3D/illustration), subject, mood, lighting, colors, composition. Min 30 words.",
      "subtitle_text": "Short on-screen text (max 8 words) to show during this scene",
      "duration_hint": "approx seconds this scene should last based on voiceover length"
    }
  ],
  "thumbnail_prompt": "Detailed image prompt for YouTube thumbnail. Bold, high contrast, eye-catching.",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
}"""

# Gemini REST endpoint
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models"
    "/{model}:generateContent?key={api_key}"
)


class ScriptGenerator:
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        self.model   = config.GEMINI_MODEL

    def generate(self, topic: str) -> dict:
        print(f"  🤖 Gemini ({self.model}) generating script for: '{topic}'")

        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"Create a complete faceless YouTube video plan.\n"
            f"Topic: {topic}\n"
            f"Niche: {config.NICHE}\n"
            f"Scenes: exactly {config.SCENES_COUNT}\n"
            f"Make voiceovers punchy, conversational, and educational. "
            f"Image prompts must be highly detailed for AI image generators like Leonardo.ai.\n"
            f"Remember: output ONLY raw JSON, nothing else."
        )

        url = GEMINI_URL.format(model=self.model, api_key=self.api_key)
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": config.MAX_TOKENS,
                "responseMimeType": "application/json"
            }
        }

        response = requests.post(url, json=payload, timeout=90)
        if response.status_code != 200:
            raise RuntimeError(
                f"Gemini API error {response.status_code}: {response.text[:300]}"
            )

        result  = response.json()
        raw     = result["candidates"][0]["content"]["parts"][0]["text"]
        clean   = re.sub(r"```json|```", "", raw).strip()
        data    = json.loads(clean)

        print(f"  ✅ Script generated: '{data['video_title']}'")
        print(f"     {len(data['scenes'])} scenes | Est. duration: {data['estimated_duration']}")
        return data
