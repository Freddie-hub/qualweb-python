from bs4 import BeautifulSoup, FeatureNotFound

def parse_html(html_content, parser_type='html.parser'):
    """
    Parses the HTML content and returns a BeautifulSoup object.

    Args:
        html_content (str): The HTML content to parse.
        parser_type (str): The parser type to use (default: 'html.parser').

    Returns:
        BeautifulSoup: Parsed BeautifulSoup object if successful, None otherwise.
    """
    try:
        soup = BeautifulSoup(html_content, parser_type)
        return soup
    except FeatureNotFound as e:
        print(f"An error occurred: {e}")
        return None

def extract_elements(soup, tag_name, class_name=None):
    """
    Extracts elements by tag name and optional class name.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object to search within.
        tag_name (str): The HTML tag name to find.
        class_name (str): Optional class name to filter by.

    Returns:
        list: A list of BeautifulSoup Tag objects.
    """
    if class_name:
        elements = soup.find_all(tag_name, class_=class_name)
    else:
        elements = soup.find_all(tag_name)
    return elements

def get_element_text(soup, tag_name, class_name=None):
    """
    Extracts and returns the text of elements by tag name and optional class name.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object to search within.
        tag_name (str): The HTML tag name to find.
        class_name (str): Optional class name to filter by.

    Returns:
        list: A list of strings containing the text of the elements.
    """
    elements = extract_elements(soup, tag_name, class_name)
    return [element.get_text(strip=True) for element in elements]

def get_attribute_value(soup, tag_name, attribute_name, class_name=None):
    """
    Extracts and returns the value of a specified attribute for elements with a given tag and optional class name.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object to search within.
        tag_name (str): The HTML tag name to find.
        attribute_name (str): The attribute name to retrieve.
        class_name (str): Optional class name to filter by.

    Returns:
        list: A list of attribute values.
    """
    elements = extract_elements(soup, tag_name, class_name)
    return [element.get(attribute_name) for element in elements if element.has_attr(attribute_name)]

def extract_links(soup):
    """
    Extracts all hyperlinks (anchor tags) from the HTML content.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object to search within.

    Returns:
        list: A list of dictionaries with 'href' and 'text' keys for each link.
    """
    links = []
    for a in soup.find_all('a', href=True):
        link = {
            'href': a['href'],
            'text': a.get_text(strip=True)
        }
        links.append(link)
    return links

def prettify_html(soup):
    """
    Returns a prettified string representation of the HTML content.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object to prettify.

    Returns:
        str: A prettified HTML string.
    """
    return soup.prettify()

if __name__ == "__main__":
    # Example usage:
    sample_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sample Page</title>
    </head>
    <body>
        <h1 class="header">Welcome to Sample Page</h1>
        <p>This is a sample paragraph with a <a href="https://example.com">link</a>.</p>
        <img src="image.jpg" alt="Sample Image">
    </body>
    </html>
    '''

    soup = parse_html(sample_html)

    if soup:
        # Extract and print all headings
        headings = get_element_text(soup, 'h1', class_name='header')
        print(f'Headings: {headings}')

        # Extract and print all links
        links = extract_links(soup)
        print(f'Links: {links}')

        # Get all image sources
        img_srcs = get_attribute_value(soup, 'img', 'src')
        print(f'Image sources: {img_srcs}')

        # Print the prettified HTML
        print(prettify_html(soup))
