"""
pipeline.py — Orchestrates the full video creation pipeline:
  Step 1: Generate script & image prompts (Claude)
  Step 2: Save image prompts to file + create placeholder images
  Step 3: Generate voiceover audio (ElevenLabs)
  Step 4: Assemble final video (MoviePy)
"""

import os
import json
import time
from datetime import datetime

from src.config import config
from src.script_generator import ScriptGenerator
from src.image_handler import ImageHandler
from src.voiceover import VoiceoverGenerator
from src.video_assembler import VideoAssembler


class VideoPipeline:
    def __init__(self, topic: str):
        self.topic = topic
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = os.path.join(config.OUTPUT_DIR, self.run_id)
        os.makedirs(self.run_dir, exist_ok=True)

    async def run(self):
        start = time.time()
        print(f"\n🚀 Starting pipeline for: '{self.topic}'")
        print(f"   Output folder: {self.run_dir}\n")

        try:
            # ── Step 1: Script ──────────────────────────────────────
            print("📋 STEP 1/4 — Generating script & image prompts")
            generator = ScriptGenerator()
            script_data = generator.generate(self.topic)
            self._save_json(script_data, "script.json")
            print()

            # ── Step 2: Images ──────────────────────────────────────
            print("🖼️  STEP 2/4 — Saving image prompts & creating placeholders")
            image_handler = ImageHandler(self.run_dir)
            image_handler.save_prompts(script_data, self.run_dir)
            image_paths = image_handler.create_placeholder_images(script_data)
            print()

            # ── Step 3: Voiceover ───────────────────────────────────
            print("🎙️  STEP 3/4 — Generating voiceover with ElevenLabs")
            voice_gen = VoiceoverGenerator(self.run_dir)
            scene_audio_paths, full_audio_path = voice_gen.generate_all(script_data)
            scene_durations = voice_gen.get_scene_durations()
            print()

            # ── Step 4: Video Assembly ──────────────────────────────
            print("🎬 STEP 4/4 — Assembling final video")
            assembler = VideoAssembler(self.run_dir)
            video_path = assembler.assemble(
                image_paths=image_paths,
                scene_audio_paths=scene_audio_paths,
                scene_durations=scene_durations,
                script_data=script_data,
                full_audio_path=full_audio_path
            )

            elapsed = time.time() - start
            self._print_summary(script_data, video_path, elapsed)

        except Exception as e:
            print(f"\n❌ Pipeline failed: {e}")
            raise

    def _save_json(self, data: dict, filename: str):
        path = os.path.join(self.run_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _print_summary(self, script_data: dict, video_path: str, elapsed: float):
        print("\n" + "="*55)
        print("   ✅  PIPELINE COMPLETE!")
        print("="*55)
        print(f"  Title    : {script_data['video_title']}")
        print(f"  Scenes   : {len(script_data['scenes'])}")
        print(f"  Time     : {elapsed:.1f}s")
        print(f"  Output   : {self.run_dir}/")
        print()
        print("  📁 Files created:")
        print(f"     script.json          → Full script data")
        print(f"     image_prompts.txt    → Paste into Leonardo.ai")
        print(f"     images/              → Placeholder images")
        print(f"     audio/               → Scene MP3s + full voiceover")
        print(f"     video/               → 🎬 Final MP4 video")
        print()
        print("  💡 Next step: Replace placeholder images with real")
        print("     AI images from Leonardo.ai / Ideogram.ai,")
        print("     then re-run just the video assembly step.")
        print("="*55 + "\n")
