import torch
from transformers import pipeline
import torchaudio
from multiprocessing import cpu_count, get_context


class WhisperTranscriber:
    def __init__(self, model_name='openai/whisper-large-v2'):
        """
        Initialize the WhisperTranscriber with a specified model.
        
        Parameters:
        - model_name (str): The name of the Whisper model to use.
        """
        self.model_name = model_name
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

    def convert_to_mono(self, waveform):
        """
        Convert stereo waveform to mono.
        
        Parameters:
        - waveform (torch.Tensor): Stereo audio waveform.
        
        Returns:
        - mono_waveform (torch.Tensor): Mono audio waveform.
        """
        if waveform.size(0) == 2:
            mono_waveform = torch.mean(waveform, dim=0, keepdim=True)
        else:
            mono_waveform = waveform
        return mono_waveform
    
    def init_worker(self):
        """
        Initialize the model pipeline in each worker process.
        """
        global pipe
        pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model_name,
            chunk_length_s=30,
            device=self.device,
        )

    def transcribe_chunk(self, audio_chunk):
        """
        Transcribe a chunk of audio.
        
        Parameters:
        - audio_chunk (dict): A dictionary with 'array' and 'sampling_rate' keys.
        
        Returns:
        - transcription (str): The transcribed text of the chunk.
        """
        prediction = pipe(audio_chunk)
        
        return prediction["text"]

    def chunk_audio(self, audio_array, sample_rate, chunk_length_s=30):
        """
        Split audio array into chunks.
        
        Parameters:
        - audio_array (np.array): The audio data.
        - sample_rate (int): The sampling rate of the audio.
        - chunk_length_s (int): Length of each chunk in seconds.
        
        Returns:
        - audio_chunks (list): List of audio chunks.
        """
        chunk_length = sample_rate * chunk_length_s
        num_chunks = len(audio_array) // chunk_length + 1
        audio_chunks = [
            {"array": audio_array[i*chunk_length:(i+1)*chunk_length], "sampling_rate": sample_rate}
            for i in range(num_chunks)
        ]
        return audio_chunks

    def transcribe(self, audio_file_path, num_workers=2):
        """
        Transcribe the given audio file using multiprocessing.
        
        Parameters:
        - audio_file_path (str): Path to the audio file to be transcribed.
        - num_workers (int): Number of worker processes to use for multiprocessing.
        
        Returns:
        - transcription (str): The transcribed text.
        """
       # Load the audio file using torchaudio
        waveform, sample_rate = torchaudio.load(audio_file_path)
        
        # Convert stereo waveform to mono if necessary
        if waveform.size(0) > 1:
            waveform = self.convert_to_mono(waveform)

        audio_array = waveform.numpy().squeeze()
        
        # Split the audio into chunks
        audio_chunks = self.chunk_audio(audio_array, sample_rate)
        
        # Set the number of worker processes
        if num_workers is None:
            num_workers = min(cpu_count(), len(audio_chunks))

        # Initialize the model pipeline in each worker and transcribe chunks in parallel
        with get_context("spawn").Pool(processes=num_workers, initializer=self.init_worker) as pool:
            transcriptions = pool.map(self.transcribe_chunk, audio_chunks)

        # Combine transcriptions
        full_transcription = " ".join(transcriptions)
        return full_transcription


if __name__ == '__main__':
    transcriber = WhisperTranscriber(model_name='openai/whisper-large-v3')
    transcription = transcriber.transcribe("./data/mono.wav", num_workers=2)
    print(transcription)