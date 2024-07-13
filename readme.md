![Icon](https://github.com/Gauff/TextProcessing/blob/master/tp_icon.png)

# Project Overview

**TLDR; Text extraction, transcription, punctuation restoration, translation, summarization and text to speech**

The goal of this project is to extend the functionalities of [Fabric](https://github.com/danielmiessler/fabric). I'm particularly interested in building pipelines using utilities like `yt` as a source and chaining them with the `|` operator in CI.

However, a major limitation exists: all operations are constrained by the LLM context. For extracting information from books, lengthy documents, or long video transcripts, content may get truncated.

To address this, I started working on adding a summarization step before applying a `fabric` template, based on the document length. 
Additionally, I explored capabilities like transcripting, translating and listening to the pipeline result or saving it as an audio file for later consumption.

## Examples

### Listen to the condensed summary of a long Youtube video
`yt --transcript url | tp --cb | tts`

### Read a web page summary
`tp --ebullets https://en.wikipedia.org/wiki/Text_processing`

### Listen to the condensed French summary of a long English Youtube video
`yt --transcript --lang en url | tp --cb --tr fr | tts`

### Save a book's wisdom as an audio file
`tp my_book.txt --eb | fabric --p extract_wisdom | tts --o my_book_wisdom.mp3` 

### Say "hello world!" in Chinese
`echo "Hello world!" | tp --tr zh | tts`

### Translate a document to Spanish
`tp doc_fr.txt --tr es > doc_es.txt`

### Generate a transcript in any language from a mp4 file. E.G.: from English to French
`tp en.mp4 --tr fr`

### Listen in spanish a French audio file
`tp fr.mp3 --tr es | tts` 

### Convert a spanish audio book to a French audio book... and make an English transcript
`tp es.mp3 --tr fr | tts --o fr.mp3 | tp fr.mp3 --tr en --o tr_en.txt`

### Extract ideas from an audio file, save them in a French text file
`tp en.mp3 | fabric --p extract_ideas | tp --tr fr --o idées.txt`

### Perform OCR
`tp image.png` 

### Extracts text from a Word file
`tp document.docx` 

# Text Processing (`tp`)

## Input (text or audio file)

`tp` receives from `stdin` or as first command line argument
It accepts:
- Text.
- File path. Supported formats are: .aiff, .bmp, .cs, .csv, .doc, .docx, .eml, .epub, .flac, .gif, .htm, .html, .jpeg, .jpg, .json, .log, .md, .mkv, .mobi, .mp3, .mp4, .msg, .odt, .ogg, .pdf, .png, .pptx, .ps, .psv, .py, .rtf, .sql, .tff, .tif, .tiff, .tsv, .txt, .wav, .xls, .xlsx

`tp` accepts unformatted content, such as automatically generated YouTube transcripts. If the text lacks punctuation, it restores it before further processing, which is necessary for chunking and text-to-speech operations.

## Transcription

Converts audio and video files to text using Whisper.

## Summarization

The primary aim is to summarize books, large documents, or long video transcripts using an LLM with an 8K context size. Various summarization levels are available:

### Extended Bullet Summary (`--ebullets`, `--eb` )

- Splits text into chunks.
- Summarizes all chunks as bullet points.
- Concatenates all bullet summaries.

The goal is to retain as much information as possible.

### Condensed Bullet Summary (`--cbullets`, `--cb`)

Executes as many `extended bullet summary` phases as needed to end up with a bullet summary smaller than an LLM context size.

### Textual Summary (`--text`, `--t`)

A simple summarization that does not rely on bullet points.

## Translation (`--translate`, `--tr`)

Translates the output text to the desired language.
Use two letters code such as `en` or `fr`.

## Usage
```
usage: tp [-h] [--ebullets] [--cbullets] [--text] [--lang LANG] [--translate TRANSLATE] [--output_text_file_path OUTPUT_TEXT_FILE_PATH] [text_or_path]

tp (text processing) provides transcription, punctuation restoration, translation and summarization from stdin, text, url, or file path. Supported file formats are: .aiff, .bmp, .cs, .csv, .doc, .docx, .eml, .epub, .flac, .gif, .htm, .html, .jpeg, .jpg, .json, .log, .md, .mkv, .mobi, .mp3, .mp4, .msg, .odt, .ogg, .pdf, .png, .pptx, .ps, .psv, .py, .rtf, .sql, .tff, .tif, .tiff, .tsv, .txt, .wav, .xls, .xlsx

positional arguments:
  text_or_path          plain text; file path; file url

options:
  -h, --help            show this help message and exit
  --ebullets, --eb      Output an extended bullet summary
  --cbullets, --cb      Output a condensed bullet summary
  --text, --t           Output a textual summary
  --lang LANG, --l LANG
                        Forced processing language. Disables the automatic detection.
  --translate TRANSLATE, --tr TRANSLATE
                        Language to translate to
  --output_text_file_path OUTPUT_TEXT_FILE_PATH, --o OUTPUT_TEXT_FILE_PATH
                        output text file path
```

# Text To Speech (`tts`)

Listen to the pipeline result or save it as an audio file to listen later.

`tts` can also read text files, automatically detecting their language.

```
usage: tts.py [-h] [--output_file_path OUTPUT_FILE_PATH] [--lang LANG] [input_text_or_path]

tts (text to speech) reads text aloud or to mp3 file

positional arguments:
  input_text_or_path    Text to read or path of the text file to read.

options:
  -h, --help            show this help message and exit
  --output_file_path OUTPUT_FILE_PATH, --o OUTPUT_FILE_PATH
                        Output file path. If none, read aloud.
  --lang LANG, --l LANG
                        Forced language. Uses language detection if not provided.
```

# Environment setup

## `.env` file
```
GROQ_API_KEY=gsk_
LITE_LLM_URI='http://localhost:4000/'
SMALL_CONTEXT_MODEL_NAME="groq/llama3-8b-8192"
SMALL_CONTEXT_MAX_TOKENS=8192
```

## script short hand

- Make script executable
`chmod +x tts.py`

- Create symlink : Link the script to a directory that's in your PATH
`sudo ln -s tts.py /usr/local/bin/tts`
