from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class ApartmentWebScraper:

    def __init__(self, discord_bot_key, whitelisted_user_ids):
        self.discord_bot_key = discord_bot_key
        self.whitelisted_user_ids = whitelisted_user_ids