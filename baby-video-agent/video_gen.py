from diffusers import StableVideoDiffusionPipeline
import torch, os
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

device = "cuda" if torch.cuda.is_available() else "cpu"
pipeline = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid", torch_dtype=torch.float16
).to(device)

def generate_clip(prompt, out_path, duration=3):
    result = pipeline(prompt, num_frames=25)
    video = result.frames[0]
    video[0].save(out_path, save_all=True, append_images=video[1:], duration=100, loop=0)

def add_text_overlay(video_path, text, output_path):
    base = VideoFileClip(video_path)
    txt = TextClip(text, fontsize=24, color='white', bg_color='black').set_position("bottom").set_duration(base.duration)
    final = CompositeVideoClip([base, txt])
    final.write_videofile(output_path, codec="libx264", audio=False, verbose=False, logger=None)

def generate_video_from_scenes(scenes, output_path):
    temp_clips = []
    for idx, scene in enumerate(scenes):
        prompt = scene['narration']
        tmp = f"scene_{idx}.mp4"
        print(f"🎥 Generating: {prompt}")
        generate_clip(prompt, tmp)
        with_text = f"text_{idx}.mp4"
        add_text_overlay(tmp, scene['scene'], with_text)
        temp_clips.append(VideoFileClip(with_text))

    final = concatenate_videoclips(temp_clips)
    final.write_videofile(output_path, codec="libx264", audio=False)

    for clip in temp_clips:
        clip.close()
    for f in os.listdir():
        if f.startswith("scene_") or f.startswith("text_"):
            os.remove(f)
