#!/usr/bin/env python3

import os
import warnings
import argparse
import sys
import text_processing
import summarize_bullets
import summarize_text
import translator
import file_management
import web
import text_extractor


# Suppress specific warnings from transformers package
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module="token_classification"
)


def main_function(options):

    raw_text = None
    if web.is_valid_url(options.text_or_path):
        raw_text = web.download_and_convert_to_md(options.text_or_path)
    else:
        is_valid_path, file_exists = file_management.check_file_path(options.text_or_path)
        
        if file_exists:
            extractor = text_extractor.UniversalTextExtractor()
            raw_text = extractor.extract(options.text_or_path, 'md')
        elif is_valid_path:
            raise FileNotFoundError(f'File [{options.text_or_path}] not found')
  
    if raw_text is None:
        return ""

    text = text_processing.punctuate_if_needed(raw_text)
    
    if options.ebullets:
        text = summarize_bullets.extended_bullet_summary(text)

    if options.cbullets:
        text = summarize_bullets.condensed_bullet_summary(text)

    if options.text:
        text = summarize_text.create_summary(text)
        
    if options.translate is not None:
        text = translator.translate(text, options.translate)

    if options.output_text_file_path is not None:
        file_management.create_text_file(text, options.output_text_file_path)

    print(text)


def main():
    parser = argparse.ArgumentParser(
        description='tp (text processing) provides transcription, punctuation restoration, translation and summarization from stdin, text, url, or file path. Supported file formats are: .aiff, .bmp, .cs, .csv, .doc, .docx, .eml, .epub, .flac, .gif, .htm, .html, .jpeg, .jpg, .json, .log, .md, .mkv, .mobi, .mp3, .mp4, .msg, .odt, .ogg, .pdf, .png, .pptx, .ps, .psv, .py, .rtf, .sql, .tff, .tif, .tiff, .tsv, .txt, .wav, .xls, .xlsx')
    
    parser.add_argument('text_or_path', 
                        nargs='?', 
                        help='plain text; audio or text file path; web page url')
    
    parser.add_argument('--ebullets', '--eb', 
                        action='store_true', 
                        help='Output an extended bullet summary')
    parser.add_argument('--cbullets', '--cb', 
                        action='store_true', 
                        help='Output a condensed bullet summary')
    parser.add_argument('--text', '--t', 
                        action='store_true', 
                        help='Output a textual summary')
    
    parser.add_argument('--translate', '--tr', 
                        action='store', 
                        help='Language to translate to',
                        required=False)
    
    parser.add_argument('--output_text_file_path', '--o',
                        action='store',
                        help='output text file path',
                        required=False)
    
    args = parser.parse_args()

    if args.text_or_path is None:
        # Read from stdin if no argument is provided
        if not sys.stdin.isatty():
            args.text_or_path = sys.stdin.read().strip()
        else:
            print("Error: No text or text file path provided and no input from stdin.")
            sys.exit(1)

    main_function(args)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.stderr.close()

