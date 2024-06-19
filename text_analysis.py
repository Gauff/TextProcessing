# Punctuated text should return >2%
def get_punctuation_percentage(text):
    if not text:
        raise ValueError("The text cannot be null or empty.")

    punctuation_marks = {'.', ',', ';', ':', '!', '?', '-', '(', ')', '[', ']', '{', '}', '"', '\'', '…'}
    total_characters = len(text)
    punctuation_count = sum(1 for char in text if char in punctuation_marks)

    return (punctuation_count / total_characters) * 100


# Example usage
# with open('D:\BibliothèqueCalibre\Lauren Bastide\Futur_es (1419)\Futur_es - Lauren Bastide - audio book.txt', 'r',
#               encoding='utf-8') as f:
#         text = f.read()
# punctuation_percentage = get_punctuation_percentage(text)
#
# print(f"Proportion of Punctuation: {punctuation_percentage:.2f}%")
