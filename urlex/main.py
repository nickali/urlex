import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import unquote, quote
import platform  # To determine the operating system
try:
    import pyperclip  # Attempt to import pyperclip
except ImportError:
    pyperclip = None  # If import fails, set pyperclip to None

def is_encoded(url):
    """
    Check if the URL is already encoded.
    If the unquoted URL differs from the original, it was encoded.
    """
    return unquote(url) != url

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    submitted_url = sys.argv[1]

    # Check if the URL is already encoded, encode if not
    if not is_encoded(submitted_url):
        encoded_url = quote(submitted_url)
    else:
        encoded_url = submitted_url

    url = 'https://urlex.org/'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        's': encoded_url
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
        soup = BeautifulSoup(response.text, 'html.parser')
        expanded_url_tag = soup.find('a', rel='external nofollow')

        if expanded_url_tag:
            expanded_url = expanded_url_tag['href']
            print()  # Print an empty line
            print(expanded_url)
            # Check if pyperclip is available and the OS is macOS
            if pyperclip and platform.system() == 'Darwin':
                pyperclip.copy(expanded_url)
                print("URL has been copied to the clipboard.")
        else:
            print("Error: Unable to find the expanded URL in the response.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

