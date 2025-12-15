# RunPod Worker for Stable-TS with Custom Yi Whisper Model

This repository contains a RunPod serverless worker implementation that uses [stable-ts](https://github.com/jianfch/stable-ts) (or the ivrit-ai fork) and the fine-tuned model `ivrit-ai/yi-whisper-large-v3`.

## Features

- **Transcription**: Full audio transcription with stable-ts.
- **Forced Alignment**: Align text with audio using `task="align"`.
- **Custom Model**: Bakes `ivrit-ai/yi-whisper-large-v3` into the Docker image for fast cold starts.

## Usage

### Build and Push

```bash
docker build -t your-username/runpod-stable-ts-yi:v1 .
docker push your-username/runpod-stable-ts-yi:v1
```

### RunPod Setup

1. Create a Serverless Endpoint on RunPod.
2. Use the image you just pushed.
3. Set container disk to at least 10GB.

### API Payload

**Transcribe (Default):**
```json
{
  "input": {
    "audio": "https://link.to/audio.mp3",
    "task": "transcribe"
  }
}
```

**Align:**
```json
{
  "input": {
    "audio": "https://link.to/audio.mp3",
    "text": "The exact text transcript corresponding to the audio...",
    "task": "align"
  }
}
```
