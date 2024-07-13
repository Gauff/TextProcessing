#!/usr/bin/env python3

import warnings
import argparse
import sys
import text_processing
import summarize_bullets
import summarize_text
import translator
import file_management
import text_extractor
from file_downloader import FileDownloader
from temporary_directory import TemporaryDirectoryManager

# Suppress specific warnings from transformers package
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module="token_classification"
)


def main_function(options):

    temporary_directory_manager = TemporaryDirectoryManager() 
    file_path = None
    raw_text = None
        
    is_valid_path, file_exists = file_management.check_file_path(options.text_or_path)
    is_url = FileDownloader.is_valid_url(options.text_or_path)

    if not is_valid_path and not is_url:
        raw_text = options.text_or_path
        
    elif is_url:
        url = options.text_or_path
        
        temporary_directory_path = temporary_directory_manager.create_temp_directory()
        
        file_downloader = FileDownloader(temporary_directory_path)
        result = file_downloader.download(url)
        
        print(result)
        
        file_path = result['file_path']
        
    elif is_valid_path:
        if not file_exists:
            raise FileNotFoundError(f'File [{options.text_or_path}] not found')
        
        file_path = options.text_or_path

    if file_path is not None:
        extractor = text_extractor.UniversalTextExtractor()
        raw_text = extractor.extract(file_path, 'md')     
  
    if raw_text is None:
        return ""

    text = text_processing.punctuate_if_needed(raw_text)
    
    forced_language_code = options.lang

    if options.ebullets:
        text = summarize_bullets.extended_bullet_summary(text, forced_language_code)

    if options.cbullets:
        text = summarize_bullets.condensed_bullet_summary(text, forced_language_code)

    if options.text:
        text = summarize_text.create_summary(text, forced_language_code)
        
    if options.translate is not None:
        text = translator.translate(text, options.translate)

    if options.output_text_file_path is not None:
        file_management.create_text_file(text, options.output_text_file_path)

    #temporary_directory_manager.remove_temp_directory()

    print(text)


def main():
    parser = argparse.ArgumentParser(
        description='tp (text processing) provides transcription, punctuation restoration, translation and summarization from stdin, text, url, or file path. Supported file formats are: .aiff, .bmp, .cs, .csv, .doc, .docx, .eml, .epub, .flac, .gif, .htm, .html, .jpeg, .jpg, .json, .log, .md, .mkv, .mobi, .mp3, .mp4, .msg, .odt, .ogg, .pdf, .png, .pptx, .ps, .psv, .py, .rtf, .sql, .tff, .tif, .tiff, .tsv, .txt, .wav, .xls, .xlsx')
    
    # input
    parser.add_argument('text_or_path', 
                        nargs='?', 
                        help='plain text; file path; file url')
    
    # summarize options
    parser.add_argument('--ebullets', '--eb', 
                        action='store_true', 
                        help='Output an extended bullet summary')
    parser.add_argument('--cbullets', '--cb', 
                        action='store_true', 
                        help='Output a condensed bullet summary')
    parser.add_argument('--text', '--t', 
                        action='store_true', 
                        help='Output a textual summary')
    
    # languages
    parser.add_argument('--lang', '--l', 
                        action='store', 
                        help='Forced processing language. Disables the automatic detection.',
                        required=False)
    
    parser.add_argument('--translate', '--tr', 
                        action='store', 
                        help='Language to translate to',
                        required=False)
        
    #output
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

