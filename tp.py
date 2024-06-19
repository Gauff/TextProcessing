# TP stands for Text Processing
import argparse

import text_processing
import summarize_bullets
import summarize_text


def extended_bullet_summary(text_or_path):
    text = text_processing.load(text_or_path)
    return summarize_bullets.extended_bullet_summary(text)


def condensed_bullet_summary(text_or_path):
    text = text_processing.load(text_or_path)
    return summarize_bullets.condensed_bullet_summary(text)


def textual_summary(text_or_path):
    text = text_processing.load(text_or_path)
    return summarize_text.create_summary(text)


def main_function(options):
    if options.ebullets:
        print(extended_bullet_summary(options.text_or_path))

    if options.cbullets:
        print(condensed_bullet_summary(options.text_or_path))

    if options.text:
        print(textual_summary(options.text_or_path))


def main():
    parser = argparse.ArgumentParser(
        description='tp (text processing) provides summarization')
    parser.add_argument('text_or_path', help='Text to summarize or path of the text file to summarize')
    parser.add_argument('--ebullets', action='store_true', help='Output an extended bullet summary')
    parser.add_argument('--cbullets', action='store_true', help='Output a condensed bullet summary')
    parser.add_argument('--text', action='store_true', help='Output textual summary')

    args = parser.parse_args()

    if args.text_or_path is None:
        print("Error: No text of text file path provided.")
        return

    main_function(args)


if __name__ == "__main__":
    main()
