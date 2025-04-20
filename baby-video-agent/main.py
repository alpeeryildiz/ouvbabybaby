import yaml
import os
from llm_script_gen import generate_script
from video_gen import generate_video_from_scenes

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

OUT_DIR = "episodes"
os.makedirs(OUT_DIR, exist_ok=True)

for ep in config["episodes"]:
    topic = ep["topic"]
    characters = ["Luna the Cat", "Max the Dog"]

    print(f"\n🧠 Generating script for: {topic} with {characters}")
    script = generate_script(topic, characters)
    print(script)

    scenes = script  # Already a list of dicts
    out_path = os.path.join(OUT_DIR, f"episode_{topic.replace(' ', '_')}.mp4")
    print("SCENE COUNT:", len(scenes))
    print("FIRST SCENE:", scenes[0] if scenes else "No scenes")

    generate_video_from_scenes(scenes, out_path)

    print(f"✅ Done: {out_path}")
