"""
video_assembler.py — Assembles images + audio into a final MP4 video.
Each scene image is shown for the duration of its voiceover audio.
Adds animated subtitle text overlays per scene.
"""

import os
from moviepy import (
    ImageClip, AudioFileClip, TextClip,
    CompositeVideoClip, concatenate_videoclips
)
from src.config import config


class VideoAssembler:
    def __init__(self, run_dir: str):
        self.videos_dir = os.path.join(run_dir, "video")
        os.makedirs(self.videos_dir, exist_ok=True)

    def assemble(
        self,
        image_paths: list[str],
        scene_audio_paths: list[str],
        scene_durations: list[float],
        script_data: dict,
        full_audio_path: str
    ) -> str:
        print(f"  🎬 Assembling video from {len(image_paths)} scenes...")

        clips = []
        for i, (img_path, audio_path, duration) in enumerate(
            zip(image_paths, scene_audio_paths, scene_durations)
        ):
            scene = script_data["scenes"][i]
            clip = self._build_scene_clip(
                img_path=img_path,
                audio_path=audio_path,
                duration=duration,
                subtitle=scene.get("subtitle_text", ""),
                scene_num=scene["number"]
            )
            clips.append(clip)
            print(f"     Scene {scene['number']} clip → {duration:.1f}s")

        final = concatenate_videoclips(clips, method="compose")

        safe_title = "".join(
            c if c.isalnum() or c in " _-" else "_"
            for c in script_data["video_title"]
        )[:50]
        output_path = os.path.join(self.videos_dir, f"{safe_title}.mp4")

        print(f"  💾 Rendering final video ({final.duration:.1f}s)... this may take a minute")
        final.write_videofile(
            output_path,
            fps=config.FPS,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile=os.path.join(self.videos_dir, "temp_audio.m4a"),
            remove_temp=True,
            logger=None
        )

        print(f"  ✅ Video saved → {output_path}")
        return output_path

    def _build_scene_clip(
        self,
        img_path: str,
        audio_path: str,
        duration: float,
        subtitle: str,
        scene_num: int
    ):
        # Base image clip sized to exact audio duration
        img_clip = (
            ImageClip(img_path)
            .with_duration(duration)
            .resized((config.VIDEO_WIDTH, config.VIDEO_HEIGHT))
        )

        # Scene audio
        audio_clip = AudioFileClip(audio_path)
        img_clip = img_clip.with_audio(audio_clip)

        layers = [img_clip]

        # Subtitle text overlay
        if subtitle:
            txt = (
                TextClip(
                    text=subtitle,
                    font_size=config.SUBTITLE_FONT_SIZE,
                    color="white",
                    stroke_color="black",
                    stroke_width=2,
                    method="caption",
                    size=(config.VIDEO_WIDTH - 200, None)
                )
                .with_duration(duration)
                .with_position(("center", config.VIDEO_HEIGHT - 160))
            )
            layers.append(txt)

        return CompositeVideoClip(layers, size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT))
