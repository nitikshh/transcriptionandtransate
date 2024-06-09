import whisper
import gradio as gr

# Load the Whisper model
model = whisper.load_model("medium")

# Define the transcription and translation function with an option for timestamps
def transcribe_and_translate(audio_file, include_timestamps):
    # Transcribe the audio
    result_transcription = model.transcribe(audio_file)
    transcription = format_segments(result_transcription["segments"], include_timestamps)
    
    # Translate the audio
    result_translation = model.transcribe(audio_file, task="translate")
    translation = format_segments(result_translation["segments"], include_timestamps)
    
    return transcription, translation

def format_segments(segments, include_timestamps):
    formatted_text = ""
    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        if include_timestamps:
            formatted_text += f"[{start:0>7.3f} --> {end:0>7.3f}]  {text}\n"
        else:
            formatted_text += f"{text}\n"
    return formatted_text

# Create the Gradio interface
iface = gr.Interface(
    fn=transcribe_and_translate,
    inputs=[
        gr.Audio(type="filepath"),
        gr.Checkbox(label="Include Timestamps")
    ],
    outputs=[
        gr.Textbox(label="Transcription"),
        gr.Textbox(label="Translation")
    ],
    title="Audio Transcription and Translation",
    description="Upload an audio file to transcribe and translate it using Whisper. Optionally, include timestamps."
)

# Launch the app
if __name__ == "__main__":
    iface.launch()
