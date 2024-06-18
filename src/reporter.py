import json
from pathlib import Path
from parse import parse_html
from fetcher import fetch_html
from checker import check_alt_attributes, check_heading_structure, check_link_texts, check_form_labels

def generate_report(alt_check_results, heading_check_results, link_text_check_results, form_label_check_results, output_format='json'):
    """
    Generates a report based on the results of accessibility checks.

    Args:
        alt_check_results (list): Results from the alt attribute check.
        heading_check_results (list): Results from the heading structure check.
        link_text_check_results (list): Results from the link text check.
        form_label_check_results (list): Results from the form label check.
        output_format (str): The format of the report ('json' or 'text').

    Returns:
        str: The generated report in the specified format.
    """
    report_data = {
        'alt_check_results': alt_check_results,
        'heading_check_results': heading_check_results,
        'link_text_check_results': link_text_check_results,
        'form_label_check_results': form_label_check_results
    }

    if output_format == 'json':
        return json.dumps(report_data, indent=4)
    elif output_format == 'text':
        return generate_text_report(report_data)
    else:
        raise ValueError("Unsupported output format. Choose either 'json' or 'text'.")

def generate_text_report(report_data):
    """
    Generates a text-based report from the report data.

    Args:
        report_data (dict): The report data from the accessibility checks.

    Returns:
        str: The generated text report.
    """
    report = []
    report.append("Accessibility Report\n")
    report.append("================================\n")

    report.append("Alt Attribute Check Results:\n")
    for item in report_data['alt_check_results']:
        report.append(f" - Image Source: {item['src']}, Has Alt: {'Yes' if item['has_alt'] else 'No'}\n")

    report.append("\nHeading Structure Check Results:\n")
    for item in report_data['heading_check_results']:
        report.append(f" - Heading: <{item['tag']}> {item['text']}, Proper Hierarchy: {'Yes' if item['is_proper'] else 'No'}\n")

    report.append("\nLink Text Check Results:\n")
    for item in report_data['link_text_check_results']:
        report.append(f" - Link Href: {item['href']}, Text: {item['text']}, Meaningful: {'Yes' if item['is_meaningful'] else 'No'}\n")

    report.append("\nForm Label Check Results:\n")
    for item in report_data['form_label_check_results']:
        report.append(f" - Input Name: {item['input']}, Has Label: {'Yes' if item['has_label'] else 'No'}\n")

    return ''.join(report)

def save_report(report, file_path):
    """
    Saves the generated report to a file.

    Args:
        report (str): The report content.
        file_path (str): The file path where the report will be saved.

    Returns:
        None
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(report)
        print(f"Report successfully saved to {file_path}")
    except IOError as e:
        print(f"An error occurred while saving the report: {e}")

if __name__ == "__main__":
    # Test script
    url = "https://example.com"
    html_content = fetch_html(url, use_selenium=False)
    if html_content:
        soup = parse_html(html_content)
        if soup:
            # Perform accessibility checks
            alt_check_results = check_alt_attributes(soup)
            heading_check_results = check_heading_structure(soup)
            link_text_check_results = check_link_texts(soup)
            form_label_check_results = check_form_labels(soup)

            # Generate and save report
            report = generate_report(
                alt_check_results,
                heading_check_results,
                link_text_check_results,
                form_label_check_results,
                output_format='json'
            )
            save_report(report, "report.json")
