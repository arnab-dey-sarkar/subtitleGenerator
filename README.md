# Subtitle Generator

A Python-based tool for generating subtitles from audio files.

## Description

This project provides a simple way to generate subtitle files (SRT format) from audio files using speech recognition technology. It supports various audio formats and can be easily integrated into larger projects.

## Features

- Support for multiple audio file formats
- Automatic speech-to-text conversion
- SRT subtitle file generation
- Easy-to-use command-line interface
- Configurable output options

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/subtitleGenerator.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install required system dependencies:
   - For Windows: Install Visual C++ Redistributable packages
   - For Linux: 
     ```bash
     sudo apt-get install portaudio19-dev python3-pyaudio
     ```

## Usage

### Command Line Interface

```bash
python transcribe.py input_audio.wav output.srt
```

### Python Library

```python
from subtitle_generator import generate_subtitles

subtitles = generate_subtitles('input_audio.wav')
subtitles.save_srt('output.srt')
```

## Requirements

- Python 3.6+
- SpeechRecognition library
- PyAudio
- Pydub
- moviepy (for audio processing)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a new Pull Request