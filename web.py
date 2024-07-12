from bs4 import BeautifulSoup
import markdownify


def convert_to_md(html):
    try:
        # Parse the HTML content
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract the HTML body content
        html_content = str(soup.body)
               
        # Convert the HTML to Markdown format
        markdown_content = markdownify.markdownify(html_content, heading_style="ATX")
        
        return markdown_content
    except Exception as e:
        return f"An error occurred during conversion: {e}"