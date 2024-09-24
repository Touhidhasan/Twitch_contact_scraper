# Twitch Scraper

This Python project is designed to scrape social media links and contact information (such as email addresses) from the "About" page of given websites using Selenium. The extracted data is then stored in a CSV file.

## Features
- Scrapes social media profiles (Instagram, Twitter, YouTube, Facebook, etc.)
- Extracts email addresses from website content
- Saves the scraped data to a CSV file
- Supports headless browsing for faster and more discreet scraping
- Easy to configure and extend

## Prerequisites

Before running the project, you need to have the following installed:
- [Python 3.x](https://www.python.org/downloads/)
- [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/)
- [Google Chrome](https://www.google.com/chrome/) (or another browser if you modify the driver)
- ChromeDriver (Make sure the version matches your Chrome browser version)

To install Selenium:
```bash
pip install selenium
