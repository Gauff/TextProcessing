from bs4 import BeautifulSoup


def remove_foot_notes(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all elements with class 'Exp'
    # (assuming footnote references are contained within elements with this class)
    footnote_references = soup.find_all('span', class_='Exp')

    # Remove footnote references
    for reference in footnote_references:
        reference.extract()

    # Find and remove the footnotes
    footnotes = soup.find_all('div', class_='_idFootnotes')
    for footnote in footnotes:
        footnote.extract()

    # Get the updated HTML content without footnotes and references
    html_without_footnotes = str(soup)

    return html_without_footnotes