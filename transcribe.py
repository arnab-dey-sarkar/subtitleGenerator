import os

# Fix Windows low-level memory/threading crashes for large models
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

import time
import sys
import tqdm
from moviepy import VideoFileClip
import torch

# Dynamically patch Whisper's internal tqdm to show a clean terminal progress bar
import whisper.transcribe


class WhisperProgressBar(tqdm.tqdm):
    def __init__(self, *args, **kwargs):
        if 'desc' not in kwargs:
            kwargs['desc'] = "Transcribing Audio"
        super().__init__(*args, **kwargs)


# Inject our custom progress tracker into the whisper system module
sys.modules['whisper.transcribe'].tqdm.tqdm = WhisperProgressBar
import whisper


# Function: Extract audio from a video file
def extract_audio(video_path, audio_output_path):
    try:
        with VideoFileClip(video_path) as video:
            video.audio.write_audiofile(audio_output_path)
        print(f"Audio has been extracted and saved as: {audio_output_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")


# Function: Transcribe audio using Whisper
def transcribe_audio(audio_path, model_type="large"):
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        print(f"Loading Whisper model '{model_type}' on {device} (this may take a moment)...")
        model = whisper.load_model(model_type, device=device)

        print("Starting transcription process...")
        # verbose=False allows our custom progress bar to dominate the screen cleanly
        result = model.transcribe(audio_path, verbose=False)
        print("\nTranscription completed!")
        return result
    except Exception as e:
        print(f"\nError during transcription: {e}")
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
                text = segment["text"].strip()

                srt_file.write(f"{i + 1}\n")
                srt_file.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
                srt_file.write(f"{text}\n\n")
        print(f"Subtitles saved as: {output_path}")
    except Exception as e:
        print(f"Error saving subtitles: {e}")


# Main workflow
def main():
    start_time = time.time()
    video_path = ""

    try:
        downloads_folder = os.path.expanduser("~/Downloads/Torrents")
        video_filename = "Masters.of.the.Universe.mkv"
        video_path = os.path.join(downloads_folder, video_filename)
        audio_output_path = os.path.join(downloads_folder, "extracted_audio.mp3")
        subtitle_output_path = os.path.join(downloads_folder, "generated_subtitles.srt")

        # Set to large model as requested
        model_type = "large"

        if not os.path.exists(video_path):
            print(f"Error: The video file does not exist at {video_path}")
            return

        # Step 1: Extract audio from the video
        print("\n=== Step 1: Extracting audio ===")
        extract_audio(video_path, audio_output_path)

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

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Calculate and display total run time execution metrics
        end_time = time.time()
        total_duration = end_time - start_time

        minutes, seconds = divmod(total_duration, 60)
        print(f"\n⏱️ Total time taken: {int(minutes)} minutes and {seconds:.2f} seconds")


# Run the program
if __name__ == "__main__":
    main()
