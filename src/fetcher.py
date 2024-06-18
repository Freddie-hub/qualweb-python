import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_html(url, use_selenium=False, wait_time=10, headless=True):
    """
    Fetches the HTML content of a web page.

    Args:
        url (str): The URL of the web page to fetch.
        use_selenium (bool): Use Selenium for dynamic content. Defaults to False.
        wait_time (int): Time to wait for dynamic content to load in seconds. Defaults to 10.
        headless (bool): Run browser in headless mode. Defaults to True.

    Returns:
        str: The HTML content of the page if successful, None otherwise.
    """
    try:
        if use_selenium:
            # Fetch HTML content using Selenium
            return fetch_html_selenium(url, wait_time, headless)
        else:
            # Fetch HTML content using Requests
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.text
    except RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return None

def fetch_html_selenium(url, wait_time, headless):
    """
    Fetches the HTML content of a web page using Selenium for dynamic content.

    Args:
        url (str): The URL of the web page to fetch.
        wait_time (int): Time to wait for dynamic content to load in seconds.
        headless (bool): Run browser in headless mode.

    Returns:
        str: The HTML content of the page.
    """
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        html_content = driver.page_source
        return html_content
    except Exception as e:
        print(f"An error occurred while fetching the URL with Selenium: {e}")
        return None
    finally:
        driver.quit()

def save_html_to_file(html_content, file_path):
    """
    Saves the HTML content to a file.

    Args:
        html_content (str): The HTML content to save.
        file_path (str): The path of the file to save the content.

    Returns:
        None
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"HTML content successfully saved to {file_path}")
    except IOError as e:
        print(f"An error occurred while saving HTML to file: {e}")

def fetch_and_save_html(url, file_path, use_selenium=False, wait_time=10, headless=True):
    """
    Fetches HTML content from a URL and saves it to a file.

    Args:
        url (str): The URL of the web page to fetch.
        file_path (str): The file path where the HTML content will be saved.
        use_selenium (bool): Use Selenium for dynamic content. Defaults to False.
        wait_time (int): Time to wait for dynamic content to load in seconds. Defaults to 10.
        headless (bool): Run browser in headless mode. Defaults to True.

    Returns:
        None
    """
    html_content = fetch_html(url, use_selenium, wait_time, headless)
    if html_content:
        save_html_to_file(html_content, file_path)
    else:
        print("Failed to fetch and save HTML content.")

if __name__ == "__main__":
    # Example usage:
    url = "https://example.com"
    file_path = "example.html"
    fetch_and_save_html(url, file_path, use_selenium=True, wait_time=10, headless=True)
