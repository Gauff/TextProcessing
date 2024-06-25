#!/usr/bin/env python3

import argparse
import my_edge_tts
import sys
import text_processing
import file_management
import languages


# prefered voices per language
voices = {
    "fr": 'fr-BE-CharlineNeural',
    "en": 'en-GB-LibbyNeural',
}


def main_function(options):
    
    if options.input_text_or_path == '':
        return
    
    text = text_processing.load(options.input_text_or_path)
    
    # Get language
    if options.lang is None:
        language = languages.get(text)
    else:
        language = options.lang
    
    # Select voice
    voice = voices.get(language, None)
    if voice is None:
        voice = my_edge_tts.get_best_matching_language_voice(language)
        
    # Command : speak or create file
    if options.output_file_path:
        command = 'tts'
        output_file_path = options.output_file_path
    else:
        command = 'playback'
        output_file_path = None
    
    temp_text_file_path = file_management.create_temp_text_file(text)    
    
    try:
        my_edge_tts.generate_mp3_file(
            temp_text_file_path,
            voice=voice,
            command=command, 
            output_mp3_file_path=output_file_path)
    except Exception as exception:
        print("Error:", exception)
    finally:
        file_management.delete_temp_file(temp_text_file_path)


def main():
    parser = argparse.ArgumentParser(
        description='tts (text to speech) reads text aloud or to mp3 file')
    parser.add_argument('input_text_or_path', 
                        nargs='?',
                        type=str, 
                        help='Text to read or path of the text file to read.')
    parser.add_argument('--output_file_path', '--o', 
                        action='store', 
                        type=str,
                        help='Output file path. If none, read aloud.', 
                        required=False)
    parser.add_argument('--lang', '--l',
                        action='store',
                        type=str,
                        help='Forced language. Uses language detection if not provided.',
                        required=False)

    args = parser.parse_args()

    args.input_text_or_path = "Hola familia, ¿cómo están?"

    if args.input_text_or_path is None:
        # Read from stdin if no argument is provided
        if not sys.stdin.isatty():
            args.input_text_or_path = sys.stdin.read().strip()
        else:
            print("Error: No text or text file path provided and no input from stdin.")
            sys.exit(1)

    main_function(args)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.stderr.close()

