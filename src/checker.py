def check_alt_attributes(soup):
    """
    Checks all <img> tags for alt attributes.

    Args:
        soup (BeautifulSoup): The parsed HTML content.

    Returns:
        list: A list of dictionaries with image src and a boolean indicating if alt text is missing.
    """
    images = soup.find_all('img')
    results = []
    for img in images:
        src = img.get('src', 'No src attribute')
        alt = img.get('alt')
        results.append({
            'src': src,
            'has_alt': bool(alt)
        })
    return results

def check_heading_structure(soup):
    """
    Checks the heading structure of the HTML content.

    Args:
        soup (BeautifulSoup): The parsed HTML content.

    Returns:
        list: A list of dictionaries with heading tag, text, and a boolean indicating proper hierarchy.
    """
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    hierarchy = {
        'h1': 1,
        'h2': 2,
        'h3': 3,
        'h4': 4,
        'h5': 5,
        'h6': 6
    }
    results = []
    previous_level = 0

    for heading in headings:
        level = hierarchy[heading.name]
        text = heading.get_text(strip=True)
        is_proper = level > previous_level or previous_level == 0
        results.append({
            'tag': heading.name,
            'text': text,
            'is_proper': is_proper
        })
        previous_level = level

    return results

def check_link_texts(soup):
    """
    Checks for meaningful link texts.

    Args:
        soup (BeautifulSoup): The parsed HTML content.

    Returns:
        list: A list of dictionaries with link href and boolean indicating meaningful text.
    """
    links = soup.find_all('a', href=True)
    results = []
    for link in links:
        href = link.get('href')
        text = link.get_text(strip=True)
        is_meaningful = bool(text and len(text) > 2)  # Assuming meaningful text is longer than 2 characters
        results.append({
            'href': href,
            'text': text,
            'is_meaningful': is_meaningful
        })
    return results

def check_form_labels(soup):
    """
    Checks if all form inputs have associated labels.

    Args:
        soup (BeautifulSoup): The parsed HTML content.

    Returns:
        list: A list of dictionaries with input name and boolean indicating presence of a label.
    """
    inputs = soup.find_all(['input', 'textarea', 'select'])
    results = []
    for input_tag in inputs:
        input_id = input_tag.get('id')
        label = soup.find('label', {'for': input_id})
        results.append({
            'input': input_tag.get('name', 'No name attribute'),
            'has_label': bool(label)
        })
    return results

if __name__ == "__main__":
    # Example usage:
    from fetcher import fetch_html
    from parse import parse_html
    
    url = "https://example.com"
    html_content = fetch_html(url, use_selenium=False)
    if html_content:
        soup = parse_html(html_content)
        if soup:
            # Check for alt attributes in images
            alt_check_results = check_alt_attributes(soup)
            print(f"Alt Attribute Check Results: {alt_check_results}")

            # Check for proper heading structure
            heading_check_results = check_heading_structure(soup)
            print(f"Heading Structure Check Results: {heading_check_results}")

            # Check for meaningful link texts
            link_text_check_results = check_link_texts(soup)
            print(f"Link Text Check Results: {link_text_check_results}")

            # Check if form inputs have associated labels
            form_label_check_results = check_form_labels(soup)
            print(f"Form Label Check Results: {form_label_check_results}")
