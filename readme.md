# SurvellAI: An Audio Analyzer for Surveillance Application

## 1) Introduction
This is a chatbot-like application that analyzes audio recordings using multiple audio models. It extracts relevant information and provides responses based on user queries into LLM assistant, enabling multiple audio-based tasks for the purposes of surveilance applications.

## 2) Supported tasks
| Tasks  | Definition  | Links  | Paper |
| :------------ |:---------------:| :-----:|  :-----:|
| Acoustic Scene Classification (ASC)  | Classify audio recording into predefined scene categories | Self-developed | [Here](https://ieeexplore.ieee.org/abstract/document/10335258/)|
| Acoustic Sound Event Detection (AED)   | Identify and localizing specific sound events in an audio recording   | Self-developed | n/a   |
| Speech-to-text (S2T) | Convert spoken language into written text   |    [Here](https://github.com/openai/whisper)    | [Here](https://arxiv.org/abs/2212.04356) |
| Language Identification (LID) | Identify spoken language    |    [Here](https://github.com/openai/whisper)    | [Here](https://arxiv.org/abs/2212.04356) |
| Speaker Diarization (SD) | Segment into speaker-specific sections |  [Here](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb)    | [Here](https://arxiv.org/abs/2106.04624) |
| Speech Emotion Recognition (SER) | Identify speaker's emotion |  [Here](https://huggingface.co/speechbrain/emotion-recognition-wav2vec2-IEMOCAP)    | [Here](https://arxiv.org/abs/2106.04624) |
| Voice Gender Detection (VGD) | Identify speaker's gender |  [Here](https://huggingface.co/JaesungHuh/voice-gender-classifier)    | [Here](https://arxiv.org/abs/2005.07143)|
| Speech Deepfake Detection (DSD) | Classifier fake or real voice |  Self-developed   | [Here](https://ieeexplore.ieee.org/abstract/document/10704095/)|
| Audio Captioning (AC) | Describe audio's content |  [Here](https://huggingface.co/wsntxxn/effb2-trm-clotho-captioning)   |[Here](https://arxiv.org/abs/2407.14329) |

## 3) Run application with Conda
### Step 1: Install conda enviroments
Env 1: asc_aed (For ASC, AED tasks)

  ```sh
  conda activate asc_aed
  pip install -r server/service_asc_aed/requirements_asc_aed.txt
  conda deactivate
  ```

Env2: whisper (For S2T, SD, SER, LID, VGD)

  ```sh
  conda activate whisper
  pip install -r server/service_whisper/requirements_whisper.txt
  conda deactivate
  ```

Env3: captioning_deepfake (For AC, DSD)

  ```sh
  conda activate captioning_deepfake
  pip install -r server/server/cap_df/requirements_captioning_df.txt
  conda deactivate
  ```

### Step 2: Get API keys
- Get your own API keys:
  - Free Grob API key for LLM from here: https://console.groq.com/keys
  - Get Pyannote access token from here: https://huggingface.co/pyannote/speaker-diarization-3.1 
- Create .env as ``server/.env``:
```sh
GROQ_API_KEY=[YOUR_GROB_API_KEY_HERE]
PYANNOTE_KEY=[YOUR_PYANNOTE_ACCESS_TOKEN_HERE]
```
### Step 3: Run 
#### Client
```sh
  conda activate whisper # activate any env has streamlit library
  cd client/
  streamlit run streamlit_app.py
  ```
#### Server
- Service ``asc_aed``: 
```sh
  conda activate asc_aed
  cd server/
  uvicorn asc_aed_API:main --host 0.0.0.0 --port 8.0.0.0
  ```
- Service ``whisper``: 
```sh
  conda activate whisper
  cd server/
  uvicorn whisper_based_API:main --host 0.0.0.0 --port 8.0.0.1
  ```

  - Service ``cap_df``: 
```sh
  conda activate captioning_deepfake
  cd server/
  uvicorn cap_df_API:main --host 0.0.0.0 --port 8.0.0.2
  ```
## 4) Run application using Docker-compose (alternative)

### Step 1: Get API keys
- Get your own API keys:
  - Free Grob API key for LLM from here: https://console.groq.com/keys
  - Get Pyannote access token from here: https://huggingface.co/pyannote/speaker-diarization-3.1 
- Create .env as ``server/.env``:
```sh
GROQ_API_KEY=[YOUR_GROB_API_KEY_HERE]
PYANNOTE_KEY=[YOUR_PYANNOTE_ACCESS_TOKEN_HERE]
```

### Step 2: Create base image
```sh
cd server/base
sudo docker build -t my_base_image -f Dockerfile.base . 
```

### Step 3: Build services and run 
```sh
sudo docker-compose up --build -d
```
