import argparse
from fetcher import fetch_html
from parse import parse_html
from checker import check_alt_attributes, check_heading_structure, check_link_texts, check_form_labels
from reporter import generate_report, save_report

def main():
    # Setting up the argument parser
    parser = argparse.ArgumentParser(description="Web Accessibility Checker Tool")
    parser.add_argument("url", help="The URL of the webpage to check")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="Format of the output report (default: json)")
    parser.add_argument("--output", required=True, help="The file path to save the report")

    # Parsing command-line arguments
    args = parser.parse_args()

    # Fetching the HTML content
    print(f"Fetching HTML content from {args.url}...")
    html_content = fetch_html(args.url, use_selenium=False)

    if not html_content:
        print("Failed to fetch HTML content. Exiting...")
        return

    # Parsing the HTML content
    print("Parsing HTML content...")
    soup = parse_html(html_content)
    if not soup:
        print("Failed to parse HTML content. Exiting...")
        return

    # Performing accessibility checks
    print("Performing accessibility checks...")
    alt_check_results = check_alt_attributes(soup)
    heading_check_results = check_heading_structure(soup)
    link_text_check_results = check_link_texts(soup)
    form_label_check_results = check_form_labels(soup)

    # Generating the report
    print(f"Generating {args.format} report...")
    report = generate_report(
        alt_check_results,
        heading_check_results,
        link_text_check_results,
        form_label_check_results,
        output_format=args.format
    )

    # Saving the report
    print(f"Saving report to {args.output}...")
    save_report(report, args.output)
    print("Report saved successfully.")

if __name__ == "__main__":
    main()
