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

    def __init__(self):
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

        pricing_view_div = self.driver.find_element(By.ID, "pricingView")

        all_units_div = pricing_view_div.find_element(By.XPATH, ".//div[2]")


        for unit_model_div in all_units_div.find_elements(By.XPATH, ".//div[@class='pricingGridItem multiFamily hasUnitGrid']"):
            for unit_div in unit_model_div.find_elements(By.XPATH, ".//div[@class='unitGridContainer mortar-wrapper ']/div[1]/ul[1]/li"):


                unit_number = unit_div.find_element(By.XPATH, ".//div[1]/div[1]/button[1]/span[2]").get_attribute('innerText').strip()
                layout_name = unit_div.get_attribute('data-model').strip()
                cost = unit_div.find_element(By.XPATH, ".//div[1]/div[2]/span[2]").get_attribute('innerText').strip()
                square_footage = unit_div.find_element(By.XPATH, ".//div[1]/div[3]/span[2]").get_attribute('innerText').strip()
                availability_outer_span = unit_div.find_element(By.XPATH, ".//div[1]/div[4]/div[1]/span[1]")

                availability_redundant_span = availability_outer_span.find_element(By.XPATH, ".//span[1]").get_attribute('innerText')
                availability_all_text = availability_outer_span.get_attribute('innerText')
                availability = availability_all_text.replace(availability_redundant_span,'',1).strip()


                available_apartments.append(ApartmentData(
                    unit_number,
                    layout_name,
                    cost,
                    square_footage,
                    availability
                ))


        return available_apartments




        
