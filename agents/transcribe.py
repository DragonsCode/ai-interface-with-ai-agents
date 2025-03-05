from openai import OpenAI

def voice_to_text(file, api_key) -> str:
    # file.seek(0)
    client = OpenAI(api_key=api_key)

    audio_file = open(file, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
    )
    audio_file.close()
    return transcription.text