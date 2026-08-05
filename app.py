import gradio as gr
import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def generate_shorts(youtube_url, num_clips=3):
    try:
        if not youtube_url or "youtube.com" not in youtube_url:
            return "❌ Invalid YouTube URL", None
        
        output_dir = Path('./output')
        if output_dir.exists():
            import shutil
            shutil.rmtree(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        cmd = [
            'python', 'main.py',
            youtube_url,
            '--mode', 'local',
            '--num-clips', str(num_clips)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        
        if result.returncode != 0:
            return f"❌ Error: {result.stderr[:300]}", None
        
        videos = sorted(output_dir.glob('short_*.mp4'))
        
        if not videos:
            return "❌ No clips generated", None
        
        msg = f"✅ Generated {len(videos)} shorts!\n\n" + "\n".join([v.name for v in videos])
        return msg, [str(v) for v in videos]
        
    except subprocess.TimeoutExpired:
        return "❌ Timeout (>30min). Try shorter video.", None
    except Exception as e:
        return f"❌ {str(e)}", None

with gr.Blocks() as demo:
    gr.Markdown("# 🎬 YouTube Shorts Generator")
    
    url = gr.Textbox(label="YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    clips = gr.Slider(1, 10, 3, step=1, label="Number of Clips")
    btn = gr.Button("🚀 Generate", variant="primary")
    
    output = gr.Textbox(label="Status", lines=5, interactive=False)
    files = gr.File(label="Download", file_count="multiple")
    
    btn.click(fn=generate_shorts, inputs=[url, clips], outputs=[output, files])

if __name__ == "__main__":
    demo.launch()
