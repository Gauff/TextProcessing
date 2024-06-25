#!/usr/bin/env python3

import argparse
import sys
import text_processing
import summarize_bullets
import summarize_text
import translator


def main_function(options):
    
    text = text_processing.load(options.text_or_path)
    
    if options.ebullets:
        text = summarize_bullets.extended_bullet_summary(text)

    if options.cbullets:
        text = summarize_bullets.condensed_bullet_summary(text)

    if options.text:
        text = summarize_text.create_summary(text)
        
    if options.translate is not None:
        text = translator.translate(text, options.translate)

    print(text)


def main():
    parser = argparse.ArgumentParser(
        description='tp (text processing) provides summarization')
    
    parser.add_argument('text_or_path', 
                        nargs='?', 
                        help='Text to summarize or path of the text file to summarize')
    
    parser.add_argument('--ebullets', '--eb', 
                        action='store_true', 
                        help='Output an extended bullet summary')
    parser.add_argument('--cbullets', '--cb', 
                        action='store_true', 
                        help='Output a condensed bullet summary')
    parser.add_argument('--text', '--t', 
                        action='store_true', 
                        help='Output textual summary')
    
    parser.add_argument('--translate', '--tr', 
                        action='store', 
                        help='Language to translate to',
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

