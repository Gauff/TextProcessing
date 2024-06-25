# pip install -U openai-whisper
# pip install setuptools-rust

# Models:
# Size 	Parameters 	English-only model 	Multilingual model
# tiny 	      39 M 	              ✓ 	✓
# base        74 M 	              ✓ 	✓
# small 	 244 M 	              ✓ 	✓
# medium 	 769 M 	              ✓ 	✓
# large 	1550 M 		                ✓

import whisper
import file_management
import torch
import numpy as np


model_names = [
    "tiny",     # 13.8 x real time : Problèmes reconnaissance Anglais, Français, grammaire
    "base",     #  8.5 x real time : Problèmes reconnaissance Anglais, Français
    "small",    #  3   x real time : Problèmes reconnaissance Anglais, Français
    "medium",   #  1.2 x real time : OK
    "large"]    #  0.7 x real time : OK


class WhisperTranscriber:
    def __init__(self, model_name='base'):
        """
        Initialize the WhisperTranscriber with a specified model.
        
        Parameters:
        - model_name (str): The name of the Whisper model to use. Options: 'tiny', 'base', 'small', 'medium', 'large'.
        """
        self.model = whisper.load_model(model_name)
    
    def transcribe(self, audio_file_path, language=None):
        """
        Transcribe the given audio file.
        
        Parameters:
        - audio_file_path (str): Path to the audio file to be transcribed.
        - language (str): The language of the audio. If None, Whisper will detect the language.
        
        Returns:
        - transcription (str): The transcribed text.
        """
        if not file_management.is_audio_file(audio_file_path):
            raise ValueError("The provided input is not a supported audio file.")
        
        # Load and preprocess the audio
        audio = whisper.load_audio(audio_file_path)
        
        # Segment the audio into 30-second chunks and transcribe each chunk
        segment_length = whisper.pad_or_trim(np.zeros(30 * 16000)).shape[0]  # 30 seconds of audio at 16000 Hz
        total_length = audio.shape[0]
        transcriptions = []
        
        for start in range(0, total_length, segment_length):
            end = min(start + segment_length, total_length)
            segment = audio[start:end]
            segment = whisper.pad_or_trim(segment)
            
            # Convert audio segment to log-Mel spectrogram
            mel = whisper.log_mel_spectrogram(segment).to(self.model.device)
            
            # Ensure the spectrogram has 128 channels
            if mel.shape[0] != 128:
                mel = self._fix_channels(mel, target_channels=128)
            
            # Detect the spoken language if not provided
            if language is None:
                _, probs = self.model.detect_language(mel)
                language = max(probs, key=probs.get)
            
            # Decode the audio segment
            options = whisper.DecodingOptions(fp16=torch.cuda.is_available(), language=language)
            result = whisper.decode(self.model, mel, options)
            transcriptions.append(result.text)
        
        # Join the transcriptions for each segment
        return " ".join(transcriptions)
    
    def _fix_channels(self, mel, target_channels=128):
        """
        Adjust the number of channels in the spectrogram to match the target number of channels.
        
        Parameters:
        - mel (torch.Tensor): The input spectrogram.
        - target_channels (int): The target number of channels.
        
        Returns:
        - mel (torch.Tensor): The adjusted spectrogram with the target number of channels.
        """
        current_channels = mel.shape[0]
        if current_channels < target_channels:
            # Pad the spectrogram with zeros to reach the target number of channels
            padding = torch.zeros((target_channels - current_channels, *mel.shape[1:]), device=mel.device)
            mel = torch.cat((mel, padding), dim=0)
        elif current_channels > target_channels:
            # Trim the spectrogram to the target number of channels
            mel = mel[:target_channels, :]
        return mel