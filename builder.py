import faster_whisper
import os
from huggingface_hub import login

def download_models():
    # Authenticate if token is present
    hf_token = os.environ.get("HF_TOKEN")
    if hf_token:
        print("HF_TOKEN found, logging in...")
        login(token=hf_token)
    else:
        print("No HF_TOKEN found, proceeding without authentication...")

    print("Starting model download...")

    # Single Requested Model
    model_id = "ivrit-ai/yi-whisper-large-v3-ct2"
    
    print(f"Downloading Whisper model: {model_id}...")
    try:
        faster_whisper.WhisperModel(model_id)
        print(f"Successfully downloaded {model_id}")
    except Exception as e:
        print(f"Error downloading {model_id}: {e}")

if __name__ == "__main__":
    download_models()
