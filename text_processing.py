import os
import punctuation
from text_analysis import get_punctuation_percentage
from langchain.text_splitter import RecursiveCharacterTextSplitter

MINIMUM_PUNCTUATION_THRESHOLD_PERCENTAGE = 1.0


def load(text_or_path):
    if os.path.isfile(text_or_path):
        return load_punctuated_text_file(text_or_path)
    return punctuate_if_needed(text_or_path)


def split(text, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "\t", "."],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.create_documents([text])

# ---


def punctuate_if_needed(text):

    if get_punctuation_percentage(text) < MINIMUM_PUNCTUATION_THRESHOLD_PERCENTAGE:
        return punctuation.restore(text)
    return text


def load_punctuated_text_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
        text = text.replace('  ', '').replace(' ', ' ')
        return punctuate_if_needed(text)
