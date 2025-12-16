import sys
import os
import logging

# Configure logging to see handler output
logging.basicConfig(level=logging.INFO)

# Add src to path so we can import handler
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    from handler import handler
except ImportError:
    print("Error: Could not import handler. Make sure you are running this from the project root and 'src/handler.py' exists.")
    sys.exit(1)

def test_transcription():
    print("\n--- Testing Transcription ---")
    # Using a short sample audio URL (public domain or common sample)
    # Using a reliable sample. 
    # If this URL fails, we can try to generate a dummy file or use another one.
    sample_audio_url = "https://github.com/kennethreitz/httpbin/blob/master/httpbin/templates/flasgger/static/swagger-ui-dist/favicon-32x32.png?raw=true" # This is a png, wait.
    # Better sample: 
    sample_audio_url = "https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav" 
    
    job = {
        "input": {
            "audio": sample_audio_url,
            "task": "transcribe",
            "language": "en" # Force English for this sample
        }
    }
    
    try:
        result = handler(job)
        print("Job Result:", result.keys() if isinstance(result, dict) else result)
        if "segments" in result:
             print(f"Success! Transcribed {len(result['segments'])} segments.")
             print("First segment:", result['segments'][0]['text'])
        elif "error" in result:
             print("Handler returned error:", result['error'])
        else:
             print("Unexpected result format.")
             
    except Exception as e:
        print(f"Exception during test: {e}")

if __name__ == "__main__":
    test_transcription()
