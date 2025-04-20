def extract_scene_prompts(script):
    scenes = []
    for scene in script:
        if isinstance(scene, dict) and 'narration' in scene and 'scene' in scene:
            scenes.append(scene)
    return scenes
