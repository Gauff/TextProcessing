# Project Overview

The goal of this project is to extend the functionalities of [Fabric](https://github.com/danielmiessler/fabric). I'm particularly interested in building pipelines using utilities like `yt` as a source and chaining them with the `|` operator in CI.

However, a major limitation exists: all operations are constrained by the LLM context. For extracting information from books, lengthy documents, or long video transcripts, content may get truncated.

To address this, I started working on adding a summarization step before applying a `fabric` template, based on the document length. Additionally, I explored capabilities like translating and listening to the pipeline result or saving it as an audio file for later consumption.

## Examples

### Listen to the condensed French summary of a long Youtube video
`yt --transcript --lang fr url | tp --cb | tts`

### Listen to the condensed French summary of a long English Youtube video
`yt --transcript --lang en url | tp --cb --tr fr | tts`

### Save a book's wisdom as an audio file
`tp my_book.txt --eb | fabric --p extract wisdom | tts --o my_book_wisdom.mp3` 

### Say "hello world!" in Chinese
`echo "Hello world!" | tp --tr zh | tts`

### Translate a document to Spanish
`tp doc_fr.txt --tr es > doc_es.txt`


# Text Processing (`tp`)

## Input text

`tp` accepts unformatted content, such as automatically generated YouTube transcripts. If the text lacks punctuation, it restores it before further processing, which is necessary for chunking and text-to-speech operations.

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
usage: tp [-h] [--ebullets] [--cbullets] [--text] [--translate TRANSLATE] [text_or_path]

tp (text processing) provides summarization

positional arguments:
  text_or_path          Text to summarize or path of the text file to summarize

options:
  -h, --help            show this help message and exit
  --ebullets, --eb      Output an extended bullet summary
  --cbullets, --cb      Output a condensed bullet summary
  --text, --t           Output textual summary
  --translate TRANSLATE, --tr TRANSLATE
                        Language to translate to
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