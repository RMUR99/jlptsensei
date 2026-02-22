from pydub import AudioSegment
from io import BytesIO
from openai import OpenAI
import os

# ------------------------------
# Windows-safe FFmpeg in project folder
# ------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = os.path.join(base_dir, "..", "ffmpeg", "ffmpeg.exe")
ffprobe_path = os.path.join(base_dir, "..", "ffmpeg", "ffprobe.exe")

print("FFmpeg path:", ffmpeg_path)
print("Exists:", os.path.isfile(ffmpeg_path))
AudioSegment.converter = ffmpeg_path
AudioSegment.ffmpeg = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path
client = OpenAI()  # reads OPENAI_API_KEY from environment
# ------------------------------
def transcribe(audio_input, filename: str | None = None):
    """
    Returns:
        {
            "text": str,
            "duration": float (seconds)
        }
    """

    if isinstance(audio_input, bytes):
        audio_input = BytesIO(audio_input)

    # ------------------------------
    # Detect format safely
    # ------------------------------
    detected_format = None

    if filename:
        ext = filename.split(".")[-1].lower()
        detected_format = ext

    try:
        if detected_format:
            audio_segment = AudioSegment.from_file(audio_input, format=detected_format)
        else:
            audio_segment = AudioSegment.from_file(audio_input)
    except Exception:
        audio_input.seek(0)
        try:
            audio_segment = AudioSegment.from_file(audio_input, format="webm")
        except Exception:
            audio_input.seek(0)
            audio_segment = AudioSegment.from_file(audio_input, format="ogg")

    # ------------------------------
    # Get duration BEFORE normalization
    # ------------------------------
    duration_seconds = len(audio_segment) / 1000.0

    # ------------------------------
    # Normalize audio
    # ------------------------------
    audio_segment = (
        audio_segment
        .set_frame_rate(16000)
        .set_channels(1)
        .set_sample_width(2)
    )

    # ------------------------------
    # Export to WAV in memory
    # ------------------------------
    buffer = BytesIO()
    audio_segment.export(buffer, format="wav")
    buffer.seek(0)

    # ------------------------------
    # Transcribe
    # ------------------------------
    transcription = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=("audio.wav", buffer, "audio/wav")
    )

    return {
        "text": transcription.text,
        "duration": duration_seconds
    }





# def transcribe(audio_input) -> str:
#     if isinstance(audio_input, bytes):
#         audio_input = BytesIO(audio_input)

#     try:
#         audio_segment = AudioSegment.from_file(audio_input)
#         buffer = BytesIO()
#         audio_segment.export(buffer, format="wav")
#         buffer.seek(0)
#     except Exception as e:
#         raise RuntimeError(f"Failed to convert audio to WAV. Make sure ffmpeg is installed: {e}")

#     try:
#         transcription = client.audio.transcriptions.create(
#             model="gpt-4o-mini-transcribe",
#             file=buffer
#         )
#         return transcription.text
#     except Exception as e:
#         raise RuntimeError(f"OpenAI transcription failed: {e}")
