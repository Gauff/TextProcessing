import os
import docx
import PyPDF2
import pytesseract
from PIL import Image
import textract
import moviepy.editor as mp
import epub_reader
from transcriber import WhisperTranscriber


class UniversalTextExtractor:

    def __init__(self):
        self.supported_formats = {
        '.aiff': self._extract_audio,
        '.bmp': self._extract_image,
        '.cs': self._extract_code,
        '.csv': self._extract_textract,
        '.doc': self._extract_textract,
        '.docx': self._extract_docx,
        '.eml': self._extract_textract,
        '.epub': self._extract_epub,
        '.flac': self._extract_audio,
        '.gif': self._extract_textract,
        '.htm': self._extract_textract,
        '.html': self._extract_textract,
        '.jpeg': self._extract_image,
        '.jpg': self._extract_image,
        '.json': self._extract_textract,
        '.log': self._extract_textract,
        '.md': self._extract_md,
        '.mkv': self._extract_video,
        '.mobi': self._extract_textract,
        '.mp3': self._extract_audio,
        '.mp4': self._extract_video,
        '.msg': self._extract_textract,
        '.odt': self._extract_textract,
        '.ogg': self._extract_textract,
        '.pdf': self._extract_pdf,
        '.png': self._extract_image,
        '.pptx': self._extract_textract,
        '.ps': self._extract_textract,
        '.psv': self._extract_textract,
        '.py': self._extract_code,
        '.rtf': self._extract_textract,
        '.sql': self._extract_code,
        '.tff': self._extract_textract,
        '.tif': self._extract_textract,
        '.tiff': self._extract_image,
        '.tsv': self._extract_textract,
        '.txt': self._extract_txt,
        '.wav': self._extract_audio,
        '.xls': self._extract_textract,
        '.xlsx': self._extract_textract,
    }

    def extract(self, file_path: str, output_format: str = 'txt') -> str:
        _, ext = os.path.splitext(file_path)
        extractor = self.supported_formats.get(ext.lower())
        if not extractor:
            raise ValueError(f"Unsupported file format: {ext}")
        
        text = extractor(file_path)
        return self._output_text(text, output_format)

    def _extract_txt(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _extract_md(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _extract_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])

    def _extract_pdf(self, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return '\n'.join([page.extract_text() for page in reader.pages])

    def _extract_epub(self, file_path: str) -> str:
        book_title, chapters_text = epub_reader.get_title_and_chapters_text(file_path)
        text = '\n\n'.join([x for x in chapters_text])
        return f'{book_title}\n\n{text}'

    def _extract_image(self, file_path: str) -> str:
        return pytesseract.image_to_string(Image.open(file_path))

    def _extract_audio(self, file_path: str) -> str:
        transcriber = WhisperTranscriber(model_name='large')
        return transcriber.transcribe(file_path)    

    def _extract_video(self, file_path: str) -> str:
        video = mp.VideoFileClip(file_path)
        audio_path = 'temp_audio.wav'
        video.audio.write_audiofile(audio_path)
        text = self._extract_audio(audio_path)
        os.remove(audio_path)
        return text

    def _extract_code(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _extract_textract(self, file_path: str) -> str:
        return textract.process(file_path).decode('utf-8')

    def _output_text(self, text: str, format: str) -> str:
        if format == 'md':
            return f"```\n{text}\n```"
        elif format == 'txt':
            return text
        else:
            raise ValueError(f"Unsupported output format: {format}")