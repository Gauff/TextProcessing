# Text Processing (`tp`)

The idea behind this project is to extend the functionalities of [Fabric](https://github.com/danielmiessler/fabric). I am particularly fond of building *pipelines* using utilities like `yt` as a source and chaining them using the `|` operator in CI.

However, there's a significant limitation: all operations are confined by the LLM context. If you want to extract information from a book, a lengthy document, or a long video transcript, the content might get truncated.

To address this, I started working on adding a summarization step before using a `fabric` template based on the document length.

## Summarization

The main idea is to summarize a book, a large document, or a long video transcript using an LLM with an 8K context size. Different summarization levels are available:

### Extended Bullet Summary (`--ebullets`)

- Splits text into chunks.
- Summarizes all chunks as bullet points.
- Concatenates all bullet summaries.

The goal is to retain as much information as possible.

### Condensed Bullet Summary (`--cbullets`)

Executes as many `extended bullet summary` phases as needed to end up with a bullet summary smaller than an LLM context size.

### Textual Summary (`--text`)

A simple summarization that does not rely on bullet points.
