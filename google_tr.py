from google.cloud import speech


def transcribe_gcs(gcs_uri, num_of_channels, language):
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        language_code=language,
        audio_channel_count=num_of_channels,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=90000)

    result_text = ""

    for result in response.results:
        result_text = result_text + result.alternatives[0].transcript
    return result_text
