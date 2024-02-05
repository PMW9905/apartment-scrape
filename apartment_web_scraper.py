from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from apartment_data import ApartmentData

default_driver_options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920x1080",
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "--disable-blink-features=AutomationControlled",
    "--enable-javascript",
    "log-level=3"
]


class ApartmentWebScraper:

    def __init__(self, discord_bot_key, whitelisted_user_ids):
        self.discord_bot_key = discord_bot_key
        self.whitelisted_user_ids = whitelisted_user_ids

        self.set_driver_options_to_default()

    def set_driver_options_to_default(self):
        self.driver_options = Options()

        for option in default_driver_options:
            self.driver_options.add_argument(option)

    def start_driver(self):
        self.driver = webdriver.Chrome(
                        service=Service(ChromeDriverManager().install()),
                        options=self.driver_options)
        
    def quit_driver(self):
        self.driver.quit()

    def dump_html(self, url):
        self.driver.get(url)
        return self.driver.find_element(By.TAG_NAME).get_attribute('innerHTML')

    def get_available_apartments_from_url(self, url):
        self.driver.get(url)

        available_apartments = []

        all_units_div = self.driver.find_element(By.CLASS_NAME, "engrainLDPunitItemList")


        for unit_div in all_units_div.find_elements(By.CLASS_NAME, "engrainLDPunitItem"):
            unit_number = unit_div.find_element(By.XPATH, ".//span[1]").get_attribute('innerText')
            layout_name = unit_div.find_element(By.XPATH, ".//span[3]").get_attribute('innerText')
            cost = unit_div.find_element(By.XPATH, ".//span[5]").get_attribute('innerText')
            unit_details = unit_div.find_element(By.XPATH, ".//span[6]").get_attribute('innerText')
            availability = unit_div.find_element(By.XPATH, ".//span[7]").get_attribute('innerText')

            available_apartments.append(ApartmentData(
                unit_number,
                layout_name,
                cost,
                unit_details,
                availability
            ))

        return available_apartments




        
