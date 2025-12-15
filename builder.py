import stable_whisper
import torch

# The user's custom fine-tuned model on Hugging Face
MODEL_ID = "ivrit-ai/yi-whisper-large-v3"

print(f"Downloading and caching model: {MODEL_ID}...")

# stable_whisper.load_model() downloads and returns the model.
# By running this during build, we cache the weights in the ~/.cache/huggingface (or similar)
# provided we ensure the cache is preserved or copying is done right in Docker.
# Ideally, we should specify a cache dir or rely on default text.
# Docker build usually persists /root/.cache/huggingface if not cleared.
model = stable_whisper.load_model(MODEL_ID)

print("Model successfully downloaded.")
