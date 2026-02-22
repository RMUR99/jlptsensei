# 🇯🇵 JLPT AI Tutor

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
│ └─ llm_engine.py # AI response generator
├─ learning/
│ ├─ vocab_tracker.py # Vocabulary tracking
│ ├─ grammar_analyzer.py # Grammar tracking
│ └─ shadowing.py # Pronunciation scoring
├─ ui/
│ ├─ chat_ui.py # Chat + shadowing UI
│ └─ dashboard.py # Learning stats dashboard
├─ voice/
│ ├─ speech_to_text.py # Convert mic audio → text (Whisper)
│ └─ text_to_speech.py # Convert text → speech (GPT TTS)
├─ data/
│ ├─ vocabulary.json # User vocab data
│ └─ grammar.json # Grammar mistakes data
├─ requirements.txt # Python dependencies
└─ README.md
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/jlpt-ai-tutor.git
cd jlpt-ai-tutor




