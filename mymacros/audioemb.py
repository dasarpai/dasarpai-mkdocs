from pathlib import Path
import os

def define_env(env):
    print(f"\n🔧 [Macros] Initializing from: {os.path.abspath(__file__)}")
    
    @env.macro
    def embed_audio(src: str, **kwargs):
        """Robust audio embed macro with enhanced error handling"""
        try:
            # Validate source path
            if not src.startswith(('http', '/', 'audio/')):
                raise ValueError(f"Invalid audio path: {src}")
                
            return f'''
            <div class="audio-container">
                <audio controls>
                    <source src="{src}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
                <div class="source-debug">Source: {src}</div>
            </div>
            '''
            
        except Exception as e:
            error_msg = f"Audio Embed Error: {str(e)}"
            print(f"⚠️ {error_msg}")
            return f'<div class="macro-error">{error_msg}</div>'

    print(f"✅ [Macros] Successfully registered embed_audio")