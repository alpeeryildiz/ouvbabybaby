def extract_scene_prompts(script: str):
    scenes = []
    current = {}
    for line in script.splitlines():
        line = line.strip()
        if line.startswith("Scene"):
            if current:
                scenes.append(current)
            current = {"scene": line.replace("Scene", "").strip(), "narration": ""}
        elif line.lower().startswith("narration"):
            current["narration"] = line.split(":", 1)[1].strip()
    if current:
        scenes.append(current)
    return scenes
