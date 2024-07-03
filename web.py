import requests
from bs4 import BeautifulSoup
import markdownify
import validators

def is_valid_url(url):
    """Check if the given string is a valid URL."""
    return validators.url(url)

def download_and_convert_to_md(url):
    """Download the content of the URL, convert to Markdown, and return as a string."""
    if not is_valid_url(url):
        return "Invalid URL provided."

    try:
        # Download the content of the URL
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the HTML body content
        html_content = str(soup.body)
               
        # Convert the HTML to Markdown format
        markdown_content = markdownify.markdownify(html_content, heading_style="ATX")
        
        return markdown_content
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the URL: {e}"