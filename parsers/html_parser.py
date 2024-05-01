from bs4 import BeautifulSoup


def extract_text_from_html(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text content
    text_content = soup.get_text(separator=' ')

    return text_content.strip()