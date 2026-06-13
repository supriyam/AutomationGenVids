"""
YouTube Faceless Video Automation Pipeline
==========================================
Generates: Script → Image Prompts → Voiceover → Final Video
"""

import asyncio
import sys
from src.pipeline import VideoPipeline
from src.config import config

def print_banner():
    print("\n" + "="*55)
    print("   🎬  YouTube Faceless Video Automation")
    print("="*55)
    print(f"  Niche     : {config.NICHE}")
    print(f"  Output Dir: ./output/")
    print("="*55 + "\n")

async def main():
    print_banner()

    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("📝 Enter your video topic: ").strip()
        if not topic:
            print("❌ No topic provided. Exiting.")
            sys.exit(1)

    pipeline = VideoPipeline(topic)
    await pipeline.run()

if __name__ == "__main__":
    asyncio.run(main())
