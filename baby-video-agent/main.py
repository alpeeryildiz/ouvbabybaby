import yaml
from llm_script_gen import generate_script
from scene_splitter import extract_scene_prompts
from video_gen import generate_video_from_scenes
import os

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

OUT_DIR = "episodes"
os.makedirs(OUT_DIR, exist_ok=True)

for ep in config["episodes"]:
    topic = ep["topic"]
    characters = ep["characters"]
    print(f"\n🧠 Generating script for: {topic} with {characters}")

    script = generate_script(topic, characters)
    print(script)

    scenes = extract_scene_prompts(script)
    out_path = os.path.join(OUT_DIR, f"episode_{topic.replace(' ', '_')}.mp4")
    generate_video_from_scenes(scenes, out_path)

    print(f"✅ Done: {out_path}")
