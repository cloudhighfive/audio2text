# Audio Transcriber 🎙️

## How It Works 🌨️

The **Audio Transcriber** tool works as follows:

1. **Finds Audio Files**: It starts by scanning a folder named `audio` to locate any audio files you’ve placed there—whether they’re in MP3, WAV, FLAC, or other common formats.
    
2. **Converts to OGG to Reduce File Size**: When it finds an audio file, it converts the file to OGG format using `ffmpeg`. This conversion is all about reducing file size. Whisper, the transcription model used here, has a file size limit. By converting the file to a more compressed format like OGG, it keeps the audio lightweight enough to fit within Whisper’s size restrictions, making it possible to handle longer audio files without cutting them down.
    
3. **Transcribes the Audio**: After converting the audio to a manageable size, the tool sends it over to Whisper for transcription. Whisper listens to the audio and generates a text version of the spoken content.
    
4. **Saves the Transcription**: The transcribed text is saved as a `.txt` file with the same name as the original audio, stored in a folder called `audio_converted`. Each audio file gets a corresponding text file, making it easy to find the transcription.

In short, **Audio Transcriber** smartly compresses and converts your audio files to keep them within Whisper’s file size limit, enabling it to handle longer recordings and provide you with organized text transcriptions, all with minimal fuss.

## Requirements 🔪

- Python 3.x
- `ffmpeg` installed on your system (for audio conversion)
- OpenAI API key (stored in a `.env` file)

## Future Plans 🤺

I(cloudhighfive 🗡️) am planning to add more features and make the tool even better, so stay tuned for updates!

Enjoy transcribing! ⚔️