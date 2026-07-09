# Selenium Test Automation

This repository contains automated test suites built using **Python**, **PyTest**, and **Selenium WebDriver** to perform end-to-end testing for a web application.

> [!NOTE]
> This repository only hosts the testing scripts. The source code of the target application (CampXchange / SellBee) is private and has not been uploaded here.

## Automated Test Cases Covered

The test suite in `test_campxchange.py` automates and validates the following workflows:

1. **Page Load Verification:** Ensures the main landing page loads correctly and verify that key container components are visible.
2. **Search Functionality:** Automates logging campus selection to local storage, navigating to the home marketplace, and verifying that the search inputs accept and process search queries.
3. **Sign-In Validation:** Verifies that form validation correctly blocks and handles invalid authentication credentials.
4. **Successful Sign-In & Verification Alert Check:** Tests valid credentials authentication flow, redirects to the home page, and validates the presence of critical elements like the email verification banner.
