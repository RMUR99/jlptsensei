from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from environment

def speak(text: str) -> bytes:
    """
    Converts text to speech and returns raw MP3 bytes.
    This handles all possible response types from OpenAI TTS.
    """
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    # Handle multiple possible types of response
    # Some older SDKs or cached responses might wrap in HttpxBinaryResponseContent
    if hasattr(response, "read"):
        # Convert streaming / binary response to raw bytes
        audio_bytes = response.read()
    elif isinstance(response, bytes):
        audio_bytes = response
    else:
        # Fallback: try __bytes__ or fail gracefully
        try:
            audio_bytes = bytes(response)
        except Exception as e:
            raise RuntimeError(f"Unable to convert TTS response to bytes: {type(response)}") from e

    return audio_bytes
