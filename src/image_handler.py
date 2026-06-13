"""
image_handler.py — Saves image prompts to files and creates placeholder images.
Since we're not using an image API, this:
  1. Saves all prompts to a readable .txt file
  2. Creates styled placeholder images with the scene title + prompt text
  3. These placeholders are used in the video; swap them with real AI images later
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap
from src.config import config


class ImageHandler:
    def __init__(self, run_dir: str):
        self.images_dir = os.path.join(run_dir, "images")
        os.makedirs(self.images_dir, exist_ok=True)
        self.image_paths: list[str] = []

    def save_prompts(self, script_data: dict, run_dir: str):
        """Save all image prompts to a nicely formatted text file."""
        prompts_path = os.path.join(run_dir, "image_prompts.txt")
        lines = [
            "=" * 60,
            f"IMAGE PROMPTS FOR: {script_data['video_title']}",
            "=" * 60,
            "",
            f"THUMBNAIL PROMPT:",
            "-" * 40,
            script_data["thumbnail_prompt"],
            "",
            "=" * 60,
            "SCENE IMAGE PROMPTS",
            "(Paste each into Leonardo.ai / Ideogram.ai / Midjourney)",
            "=" * 60,
            ""
        ]
        for scene in script_data["scenes"]:
            lines += [
                f"Scene {scene['number']}: {scene['title']}",
                "-" * 40,
                scene["image_prompt"],
                "",
            ]
        with open(prompts_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"  📄 Image prompts saved → {prompts_path}")
        return prompts_path

    def create_placeholder_images(self, script_data: dict) -> list[str]:
        """Create styled placeholder images for each scene."""
        print(f"  🖼️  Creating {len(script_data['scenes'])} placeholder images...")
        colors = [
            "#1a1a2e", "#16213e", "#0f3460", "#1b262c",
            "#0d1b2a", "#1c2541"
        ]
        for i, scene in enumerate(script_data["scenes"]):
            path = self._make_image(
                scene_num=scene["number"],
                title=scene["title"],
                subtitle=scene.get("subtitle_text", ""),
                prompt_hint=scene["image_prompt"][:80] + "...",
                color=colors[i % len(colors)]
            )
            self.image_paths.append(path)
            print(f"     Scene {scene['number']} placeholder created")
        return self.image_paths

    def _make_image(self, scene_num, title, subtitle, prompt_hint, color) -> str:
        w, h = config.VIDEO_WIDTH, config.VIDEO_HEIGHT
        img = Image.new("RGB", (w, h), color=color)
        draw = ImageDraw.Draw(img)

        # Gradient overlay effect with rectangles
        for y in range(0, h, 4):
            alpha = int(30 * (y / h))
            draw.rectangle([0, y, w, y + 4], fill=self._darken(color, alpha))

        # Scene number badge
        draw.rectangle([80, 80, 200, 140], fill="#ffffff20", outline="#ffffff40", width=1)
        draw.text((140, 110), f"SCENE {scene_num}", fill="#aaaaaa", anchor="mm",
                  font=self._font(22))

        # Main title
        title_lines = textwrap.wrap(title.upper(), width=28)
        y_start = h // 2 - (len(title_lines) * 70) // 2
        for line in title_lines:
            draw.text((w // 2, y_start), line, fill="#ffffff", anchor="mm",
                      font=self._font(72))
            y_start += 80

        # Subtitle
        if subtitle:
            draw.text((w // 2, h // 2 + 120), subtitle, fill="#88ccff",
                      anchor="mm", font=self._font(38))

        # Bottom prompt hint
        hint_lines = textwrap.wrap(f"📸 {prompt_hint}", width=90)
        y_hint = h - 120
        for line in hint_lines[:2]:
            draw.text((w // 2, y_hint), line, fill="#555555", anchor="mm",
                      font=self._font(20))
            y_hint += 28

        # Bottom watermark
        draw.text((w // 2, h - 40), "⚡ Replace with AI-generated image",
                  fill="#333333", anchor="mm", font=self._font(20))

        filename = os.path.join(self.images_dir, f"scene_{scene_num:02d}.png")
        img.save(filename, "PNG")
        return filename

    def _font(self, size: int):
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        except:
            try:
                return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
            except:
                return ImageFont.load_default()

    def _darken(self, hex_color: str, amount: int) -> str:
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = max(0, r - amount)
        g = max(0, g - amount)
        b = max(0, b - amount)
        return f"#{r:02x}{g:02x}{b:02x}"
