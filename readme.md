# LLM-guided Audio Surveillance Application

## Introduction
- This is a chatbot-like application that analyzes audio recordings using multiple audio models. It extracts relevant information and provides responses based on user queries into LLM assistant, enabling multiple audio-based tasks for the purposes of surveilance applications.

## Supported tasks
| Tasks  | Definition  | Links  | Paper |
| :------------ |:---------------:| :-----:|  :-----:|
| Acoustic Scene Classification (ASC)  | Classify audio recording into predefined scene categories | Self-developed | https://ieeexplore.ieee.org/abstract/document/10335258/|
| Acoustic Sound Event Detection (AED)   | Identify and localizing specific sound events in an audio recording   | Self-developed | n/a   |
| Speech-to-text (S2T) | Convert spoken language into written text   |    https://github.com/openai/whisper    | https://arxiv.org/abs/2212.04356 |
| Language Identification (LID) | Identify spoken language    |    https://github.com/openai/whisper    | https://arxiv.org/abs/2212.04356 |
| Speaker Diarization (SD) | Segment into speaker-specific sections |  https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb    | [https://arxiv.org/abs/2106.04624](https://arxiv.org/abs/2106.04624) |
| Speech Emotion Recognition (SER) | Identify speaker's emotion |  https://huggingface.co/speechbrain/emotion-recognition-wav2vec2-IEMOCAP    | [https://arxiv.org/abs/2106.04624](https://arxiv.org/abs/2106.04624) |
| Voice Gender Detection (VGD) | Identify speaker's gender |  https://huggingface.co/JaesungHuh/voice-gender-classifier    | https://arxiv.org/abs/2005.07143|
| Speech Deepfake Detection (DSD) | Classifier fake or real voice |  Self-developed   | https://ieeexplore.ieee.org/abstract/document/10704095/|
| Audio Captioning (AC) | Describe audio's content |  https://huggingface.co/wsntxxn/effb2-trm-clotho-captioning   |https://arxiv.org/abs/2407.14329 |

## Run application
### 1) Install conda enviroments
Env 1: asc_aed (For ASC, AED tasks)

  ```sh
  conda activate asc_aed
  pip install -r server/requirements_asc_aed.txt
  conda deactivate
  ```

Env2: whisper (For S2T, SD, SER, LID, VGD)

  ```sh
  conda activate whisper
  pip install -r server/requirements_whisper.txt
  conda deactivate
  ```

Env3: captioning_deepfake (For AC, DSD)

  ```sh
  conda activate captioning_deepfake
  pip install -r server/requirements_captioning_df.txt
  conda deactivate
  ```

### 2) GET API KEYS
- Get your own API keys:
  - Free Grob API key for LLM from here: https://console.groq.com/keys
  - Get Pyannote access token from here: https://huggingface.co/pyannote/speaker-diarization-3.1 
- Create .env as server/.env:
```sh
GROQ_API_KEY=[YOUR_GROB_API_KEY_HERE]
PYANNOTE_KEY=[YOUR_PYANNOTE_ACCESS_TOKEN_HERE]
```
### 3) Run 
#### Client
```sh
  conda activate whisper
  cd client/
  streamlit run streamlit_app.py
  ```
#### Server
```sh
  conda activate whisper
  cd server/
  uvicorn api:main --host 0.0.0.0 --port 8.0.0.0
  ```

### Run application using Docker-compose
...

