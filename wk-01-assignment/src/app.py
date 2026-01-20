"""
Coffee Shop System - Flask Application with Manim Animations
Demonstrates stocks, flows, and feedback loops in a coffee shop system.
"""
from flask import Flask, render_template, send_from_directory, url_for
import os
import subprocess
import sys

app = Flask(__name__)

# Directory for rendered animations (Manim default output structure)
MEDIA_DIR = os.path.join(os.path.dirname(__file__), 'media', 'videos', 'scenes', '480p15')

# Animation metadata
ANIMATIONS = {
    'stocks-flows': {
        'title': 'Stocks & Flows Dynamic',
        'description': 'Watch how inflows and outflows dynamically change stock levels through the day.',
        'scene': 'StocksFlowsDynamicScene'
    },
    'feedback-loops': {
        'title': 'Feedback Loops',
        'description': 'Explore both reinforcing (Word of Mouth) and balancing (Wait Time) feedback loops.',
        'scene': 'FeedbackLoopsScene'
    },
    'full-system': {
        'title': 'Complete System Overview',
        'description': 'The entire coffee shop system with all stocks, flows, and feedback loops.',
        'scene': 'FullSystemScene'
    }
}


def render_animation(scene_name):
    """Render a Manim scene if the video doesn't exist."""
    # Manim outputs to media/videos/<filename>/480p15/<scene_name>.mp4 by default
    scenes_file = os.path.join(os.path.dirname(__file__), 'scenes.py')
    output_dir = os.path.join(os.path.dirname(__file__), 'media', 'videos', 'scenes', '480p15')
    video_path = os.path.join(output_dir, f'{scene_name}.mp4')
    
    if not os.path.exists(video_path):
        print(f"Rendering {scene_name}... This may take a moment.")
        
        # Render the scene using manim
        result = subprocess.run([
            sys.executable, '-m', 'manim', 'render',
            '-ql',  # Low quality (480p15) for faster rendering
            scenes_file,
            scene_name
        ], cwd=os.path.dirname(__file__), capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Manim error: {result.stderr}")
            raise Exception(f"Failed to render {scene_name}: {result.stderr}")
        
        print(f"Rendered {scene_name} successfully!")
    
    return video_path


@app.route('/')
def index():
    """Home page with navigation to all animations."""
    return render_template('index.html', animations=ANIMATIONS)


@app.route('/animation/<animation_id>')
def animation(animation_id):
    """Display a specific animation."""
    if animation_id not in ANIMATIONS:
        return "Animation not found", 404
    
    anim_info = ANIMATIONS[animation_id]
    scene_name = anim_info['scene']
    
    # Render the animation if needed
    try:
        render_animation(scene_name)
        video_url = url_for('serve_video', filename=f'{scene_name}.mp4')
    except Exception as e:
        video_url = None
        print(f"Error rendering animation: {e}")
    
    return render_template('animation.html', 
                          animation=anim_info,
                          animation_id=animation_id,
                          video_url=video_url)


@app.route('/media/<path:filename>')
def serve_video(filename):
    """Serve rendered video files."""
    return send_from_directory(MEDIA_DIR, filename)


if __name__ == '__main__':
    print("🍵 Coffee Shop System Demo")
    print("=" * 40)
    print("Starting Flask server...")
    print("Open http://localhost:5000 in your browser")
    print("=" * 40)
    app.run(debug=True, port=5000)
