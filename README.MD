# JLPT AI Tutor 日本語能力試験の先生

## Project Overview

**JLPT AI Tutor** is a Python-based Streamlit application designed for self-study of Japanese.  
It combines **text chat, voice interaction, shadowing practice, vocabulary tracking, and grammar analysis**.  
Users can chat in Japanese, practice JLPT-level sentences, and get instant feedback on pronunciation.

**Key Features:**
- Chat with AI in Japanese (text + voice)  
- Shadowing practice for pronunciation improvement  
- JLPT level selection (N5 → N1)  
- Vocabulary tracking & grammar analysis  
- Voice output powered by OpenAI GPT-4o-mini-tts  
- Speech-to-text using OpenAI Whisper  
- Pronunciation similarity scoring  

---

## Project Structure
```JLPT_AI_Tutor/
├─ app.py # Main Streamlit entry
├─ core/
│ └─ llm_engine.py ( LLM handling TTS , STT )
  └─ exam_engine.py ( hashlib to create new questions )
　└─ jlpt_rules.py (list of jlpt levels ) 
  └─ prompt_builder.py (prompt for llm engine and exam engine formats ) 
├─ learning/
│ ├─ vocab_tracker.py # Vocabulary tracking
│ ├─ grammar_analyzer.py # Grammar tracking
│ └─ shadowing.py # Pronunciation scoring
  └─ exam_tracker.py # Exam  scoring
├─ ui/
│ ├─ chat_ui.py # Chat + shadowing UI
│ └─ dashboard.py # Learning stats dashboard
  └─  exam_ui.py # Exam UI
├─ ffmpeg/
│ ├─ ffmpeg.exe # audio handling
│ ├─ ffmprobe.exe
│ 
├─ voice/
│ ├─ speech_to_text.py # Convert mic audio → text (Whisper)
│ └─ text_to_speech.py # Convert text → speech (GPT TTS)
├─ data/
│ ├─ vocabulary.json # User vocab data
│ └─ grammar.json # Grammar mistakes data
  └─ exam_tracker.json # exam scores data storages
├─ requirements.txt # Python dependencies
└─ README.md
```

## Installation
Downldling Fmpeg >> bin >> you will find 2 .exe files one for `ffmpeg` and the other for `ffrope` and you can simply copy them to your project 
download link : https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z

1. **Clone the repository**
```bash
git clone https://github.com/RMUR99/jlptsensei.git
cd jlptsensei




