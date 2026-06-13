"""
voiceover.py — Generates per-scene MP3 audio using ElevenLabs API,
then combines them into one full voiceover track.
"""

import os

import numpy as np
import requests
from moviepy.audio.AudioClip import AudioClip, concatenate_audioclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from src.config import config


ELEVENLABS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


class VoiceoverGenerator:
    def __init__(self, run_dir: str):
        self.audio_dir = os.path.join(run_dir, "audio")
        os.makedirs(self.audio_dir, exist_ok=True)
        self.scene_audio_paths: list[str] = []

    def generate_all(self, script_data: dict) -> tuple[list[str], str]:
        """Generate audio for each scene, then merge into one file."""
        print(f"  🎙️  Generating voiceover for {len(script_data['scenes'])} scenes...")

        for scene in script_data["scenes"]:
            path = self._generate_scene_audio(
                text=scene["voiceover"],
                scene_num=scene["number"]
            )
            self.scene_audio_paths.append(path)

        merged_path = self._merge_audio()
        return self.scene_audio_paths, merged_path

    def _generate_scene_audio(self, text: str, scene_num: int) -> str:
        url = ELEVENLABS_URL.format(voice_id=config.ELEVENLABS_VOICE_ID)
        headers = {
            "xi-api-key": config.ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
        payload = {
            "text": text,
            "model_id": config.ELEVENLABS_MODEL,
            "voice_settings": {
                "stability": config.VOICE_STABILITY,
                "similarity_boost": config.VOICE_SIMILARITY
            }
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        if response.status_code != 200:
            raise RuntimeError(
                f"ElevenLabs error on scene {scene_num}: "
                f"{response.status_code} — {response.text[:200]}"
            )

        path = os.path.join(self.audio_dir, f"scene_{scene_num:02d}.mp3")
        with open(path, "wb") as f:
            f.write(response.content)

        size_kb = os.path.getsize(path) // 1024
        print(f"     Scene {scene_num} audio → {size_kb} KB")
        return path

    def _merge_audio(self) -> str:
        """Concatenate all scene audio files with a short pause between scenes."""
        print("  🔗 Merging all scene audio files...")

        if not self.scene_audio_paths:
            raise RuntimeError("No scene audio files to merge")

        first_segment = AudioFileClip(self.scene_audio_paths[0])
        channels = first_segment.nchannels
        first_segment.close()

        silence = AudioClip(
            lambda t: np.zeros((len(t), channels)),
            duration=0.6,
            fps=44100
        )

        clips = []
        for path in self.scene_audio_paths:
            segment = AudioFileClip(path)
            clips.append(segment)
            clips.append(silence)

        combined = concatenate_audioclips(clips)
        output_path = os.path.join(self.audio_dir, "full_voiceover.mp3")
        combined.write_audiofile(output_path, fps=44100, codec="libmp3lame")
        duration_s = combined.duration
        print(f"  ✅ Full voiceover: {duration_s:.1f}s → {output_path}")
        return output_path

    def get_scene_durations(self) -> list[float]:
        """Return duration in seconds for each scene audio file."""
        durations = []
        for path in self.scene_audio_paths:
            seg = AudioFileClip(path)
            durations.append(seg.duration + 0.6)
            seg.close()
        return durations
