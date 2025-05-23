import os
from moviepy.editor import VideoFileClip
import torch
import whisper

# Function: Extract audio from a video file
def extract_audio(video_path, audio_output_path):
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_output_path)
        print(f"Audio has been extracted and saved as: {audio_output_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")

# Function: Transcribe audio using Whisper
def transcribe_audio(audio_path, model_type="large"):
    try:
        # Detect if GPU is available, otherwise fallback to CPU
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        # Load Whisper model
        print(f"Loading Whisper model '{model_type}' on {device}...")
        model = whisper.load_model(model_type, device=device)

        # Transcribe audio
        result = model.transcribe(audio_path)
        print("Transcription completed!")
        return result
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

# Function: Save transcription results as a `.srt` subtitle file
def save_subtitles(segments, output_path):
    try:
        def format_timestamp(seconds):
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = int((seconds % 1) * 1000)
            return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

        with open(output_path, "w", encoding="utf-8") as srt_file:
            for i, segment in enumerate(segments):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]

                srt_file.write(f"{i+1}\n")
                srt_file.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
                srt_file.write(f"{text}\n\n")
        print(f"Subtitles saved as: {output_path}")
    except Exception as e:
        print(f"Error saving subtitles: {e}")

# Main workflow
def main():
    try:
        # Paths
        downloads_folder = os.path.expanduser("~/Downloads/Torrents")  # Path to Downloads folder
        video_filename = "Thunderbolts.mp4"  # Replace with the name of your video file
        video_path = os.path.join(downloads_folder, video_filename)
        audio_output_path = os.path.join(downloads_folder, "extracted_audio.mp3")
        subtitle_output_path = os.path.join(downloads_folder, "generated_subtitles.srt")

        # Whisper model type: Use "large" for highest transcription accuracy
        model_type = "large"

        # Step 1: Extract audio from the video
        print("\n=== Step 1: Extracting audio ===")
        # extract_audio(video_path, audio_output_path)

        # Step 2: Transcribe audio to text using Whisper
        print("\n=== Step 2: Transcribing audio ===")
        result = transcribe_audio(audio_path=audio_output_path, model_type=model_type)

        if result is None:
            print("Transcription failed. Exiting...")
            return

        # Step 3: Save subtitles to an SRT file
        print("\n=== Step 3: Saving subtitles ===")
        save_subtitles(result["segments"], subtitle_output_path)

        print("\nProcess completed successfully!")
    except FileNotFoundError:
        print(f"File not found: {video_path}. Please check the filename and path!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the program
if __name__ == "__main__":
    main()