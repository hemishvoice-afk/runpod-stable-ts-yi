import runpod
import stable_whisper
import base64
import os
import tempfile
import torch

# Load model globally for warm starts
MODEL_ID = "ivrit-ai/yi-whisper-large-v3-ct2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading model {MODEL_ID} on {DEVICE}...")
try:
    # Load the model we baked in builder.py
    model = stable_whisper.load_faster_whisper(MODEL_ID, device=DEVICE)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    # Fallback or exit? For serverless, better to fail fast.
    raise e

def handler(job):
    """
    Handler for RunPod serverless worker.
    Input format:
    {
        "input": {
            "audio": "base64_string" or "http_url",
            "text": "plain text for alignment (optional)",
            "task": "transcribe" (default) or "align",
            "language": "he" (optional, default auto)
        }
    }
    """
    job_input = job.get('input', {})
    
    # Extract inputs
    audio_input = job_input.get('audio')
    text_input = job_input.get('text')
    task = job_input.get('task', 'transcribe')
    language = job_input.get('language') 
    
    if not audio_input:
        return {"error": "No 'audio' provided in input."}

    # Prepare audio source (path to temp file or URL)
    temp_audio_path = None
    audio_source = audio_input
    
    try:
        # Check if input is base64 (simple heuristic: no "http" prefix and long string)
        # However, users might pass just a path? Assume URL or Base64.
        if not audio_input.startswith('http'):
            # Decode base64 to temp file
            # We assume mp3 or wav. stable-ts/ffmpeg handles headers usually.
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
                # Handle possible data URI scheme prefix (e.g. "data:audio/mp3;base64,...")
                if "," in audio_input:
                    audio_input = audio_input.split(",", 1)[1]
                
                tf.write(base64.b64decode(audio_input))
                temp_audio_path = tf.name
                audio_source = temp_audio_path
        
        print(f"Processing task: {task} with language: {language}")
        
        result_dict = {}
        
        if task == 'align':
            if not text_input:
                return {"error": "Task is 'align' but no 'text' provided."}
            
            # Perform alignment
            # align() takes audio and text.
            # language ensures we use the right tokenizer/alphabet.
            alignment_result = model.align(
                audio_source, 
                text_input, 
                language=language
            )
            result_dict = alignment_result.to_dict()
            
        else:
            # Default to transcribe
            transcription_result = model.transcribe(
                audio_source, 
                language=language
            )
            result_dict = transcription_result.to_dict()

        return result_dict

    except Exception as e:
        print(f"Error processing job: {e}")
        return {"error": str(e)}
        
    finally:
        # Cleanup temp file
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
