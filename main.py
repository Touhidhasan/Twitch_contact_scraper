import time
import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class SocialMediaScraper:
    """
    Class to scrape social media links and contact information from a given website.
    """

    def __init__(self, driver_path, headless=True):
        """
        Initialize the web scraper with a Chrome WebDriver.

        :param driver_path: Path to the ChromeDriver executable.
        :param headless: Boolean to decide whether to run the browser in headless mode.
        """
        chrome_options = webdriver.ChromeOptions()

        # Use Service to specify the driver path
        service = Service(driver_path)
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")

        # Initialize WebDriver
        self.driver = webdriver.Chrome(service=service)

    def search_data(self, url):
        """
        Scrape social media and contact links from the "About" page of a given URL.

        :param url: The base URL of the website.
        :return: Dictionary containing the scraped data.
        """
        about_page = f"{url}/about"
        self.driver.get(about_page)
        time.sleep(1)  # Pause to allow page to load

        data = {
            'url': url,
            'instagram': self.get_element_link("//a[contains(@href,'instagram.com')]"),
            'twitter': self.get_element_link("//a[contains(@href,'twitter.com')]"),
            'youtube': self.get_element_link("//a[contains(@href,'youtube.com')]"),
            'facebook': self.get_element_link("//a[contains(@href,'facebook.com')]"),
            'discord': self.get_element_link("//p[normalize-space()='Discord']/../.."),
            'reddit': self.get_element_link("//a[contains(@href,'reddit.com')]"),
            'tiktok': self.get_element_link("//a[contains(@href,'tiktok.com')]"),
            'vk': self.get_element_link("//a[contains(@href,'vk.com')]"),
            'spotify': self.get_element_link("//a[contains(@href,'spotify.com')]"),
            'linktr': self.get_element_link("//a[contains(@href,'linktr.ee')]"),
            'website': self.get_element_link("//p[normalize-space()='Website']/../.."),
            'email': self.get_email()
        }

        return data

    def get_element_link(self, xpath):
        """
        Retrieve the href attribute of an element using XPath.

        :param xpath: The XPath string to locate the element.
        :return: The href link of the element or an empty string if not found.
        """
        try:
            return self.driver.find_element("xpath", xpath).get_attribute("href")
        except:
            return ""

    def get_email(self):
        """
        Extract an email address from the webpage content.

        :return: The extracted email or an empty string if not found.
        """
        try:
            email_text = self.driver.find_element("xpath", "//p[contains(text(),'@')]").text
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", email_text)
            return emails[0] if emails else ""
        except:
            return ""

    def write_to_csv(self, file_name, data, mode='a'):

        # Write scraped data to a CSV file.

        with open(file_name, mode, newline='', encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            if mode == 'w':  # Write header if creating a new file
                writer.writerow(
                    ["url", "instagram", "twitter", "youtube", "facebook", "discord", "reddit", "tiktok", "vk",
                     "spotify", "linktr", "website", "email"])
            for row in data:
                writer.writerow(
                    [row['url'], row['instagram'], row['twitter'], row['youtube'], row['facebook'], row['discord'],
                     row['reddit'], row['tiktok'], row['vk'], row['spotify'], row['linktr'], row['website'],
                     row['email']])

    def scrape_urls(self, input_file, output_file):
        """
        Scrape data from a list of URLs in an input CSV file and write results to an output CSV file.

        :param input_file: The path to the CSV file containing the list of URLs to scrape.
        :param output_file: The path to the CSV file where the scraped data will be saved.
        """
        self.write_to_csv(output_file, [], mode='w')  # Create output CSV with header
        with open(input_file, 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader, start=1):
                url = row[0]
                print(f"Sl. {i}: {url}")
                data = self.search_data(url)
                self.write_to_csv(output_file, [data])

    def close(self):
        """
        Close the WebDriver instance
        """
        self.driver.quit()


if __name__ == "__main__":
    # Initialize the scraper
    driver_path = 'chromedriver.exe'
    scraper = SocialMediaScraper(driver_path)

    # Input and output CSV files
    input_file = 'input.csv'
    output_file = 'output.csv'

    # Start scraping
    scraper.scrape_urls(input_file, output_file)

    # Close the driver
    scraper.close()
