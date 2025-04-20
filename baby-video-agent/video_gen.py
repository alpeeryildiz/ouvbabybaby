from diffusers import DiffusionPipeline
import torch, os
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from diffusers import DiffusionPipeline

pipeline = DiffusionPipeline.from_pretrained(
    "cerspense/zeroscope_v2_576w", torch_dtype=torch.float16
).to("cuda")

def generate_clip(prompt, out_path, num_frames=25, fps=8):
    video_frames = pipeline(prompt).frames[0]  # list of PIL images
    video_frames[0].save(
        out_path,
        save_all=True,
        append_images=video_frames[1:],
        duration=int(1000 / fps),
        loop=0
    )
def add_text_overlay(video_path, text, output_path):
    base = VideoFileClip(video_path)
    txt = TextClip(text, fontsize=24, color='white', bg_color='black') \
            .set_position("bottom").set_duration(base.duration)
    final = CompositeVideoClip([base, txt])
    final.write_videofile(output_path, codec="libx264", audio=False, verbose=False, logger=None)
    base.close()
    final.close()

def generate_video_from_scenes(scenes, output_path):
    temp_clips = []

    for idx, scene in enumerate(scenes):
        prompt = scene.get('narration', '').strip()
        if not prompt:
            print(f"⚠️ Scene {idx} skipped: empty narration.")
            continue

        tmp = f"scene_{idx}.mp4"
        print(f"🎥 Generating scene {idx + 1}: {prompt}")
        try:
            generate_clip(prompt, tmp)
            with_text = f"text_{idx}.mp4"
            add_text_overlay(tmp, scene.get('scene', f"Scene {idx + 1}"), with_text)
            temp_clips.append(VideoFileClip(with_text))
        except Exception as e:
            print(f"⚠️ Skipping scene {idx} due to error: {e}")

    if not temp_clips:
        raise ValueError("🚫 No valid video clips were generated. Check your prompts and model output.")

    final = concatenate_videoclips(temp_clips)
    final.write_videofile(output_path, codec="libx264", audio=False)

    for clip in temp_clips:
        clip.close()
    for f in os.listdir():
        if f.startswith("scene_") or f.startswith("text_"):
            os.remove(f)
