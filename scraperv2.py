import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta

class MaximaScraper:

    def __init__(self, date):
        self.date = date
        self.data = []

        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--disable-extension")
        self.options.add_argument("--dns-prefetch-disable")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--silent")
        self.options.add_argument("--disable-infobars")

    def get_driver(self) -> webdriver:
        """Gets driver for website.

        :return: driver (webdriver) object with preloaded maxima discount website.
        """
        driver = webdriver.Chrome(options=self.options)
        driver.get("https://www.maxima.lt/akcijos")

        # Click cookies if applicable
        try:
            driver.find_element(by=By.XPATH, value="""//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]""").click()
        except:
            print("No cookie button exists")

        return driver

    def get_upload_date(self) -> np.array:
        """Gets the dates of the week that the scraper grabs"""
        start = date.today() - timedelta(days=date.today().weekday())
        end  = start + timedelta(days=6)
        return [start, end]

    def upload(self, df):
        """Saves data to csv file.

        :param df: df (pd.DataFrame).
        """

        dates = self.get_upload_date()
        df.to_csv(f"maxima-discounts/{dates[0]}_maxima_{dates[1]}.csv", sep=';')

    def postprocessing(self, data) -> pd.DataFrame:
        """Applies postprocessing to data.

        :param data: array with dictionaries with discount data.
        :return: df (pd.DataFrame) with processed values.
        """
        df = pd.DataFrame(data)
        df["Image_link"].fillna(df["Image_link_visible"], inplace=True)

        df.drop(columns=["Image_link_visible"], inplace=True)

        for col in df.columns:
            if df[col].dtype == "object":
                print(col)
                df[col] = df[col].str.replace("€", '').str.replace(', nuo', ' ').str.strip()


        return df

    def scrape_maxima(self, driver):
        """Scrapes Maxima Discount page with all the information in it.

        :param driver: Webdriver with open Maxima discount page.
        """
        for category in driver.find_elements(By.CLASS_NAME, value="my-5"):
            category_name = category.find_element(By.TAG_NAME, value="h2").get_attribute("textContent")

            print(f"Scraping {category_name} category")
            for discount_item in category.find_elements(By.CLASS_NAME, value="card-body"):
                discount_data = {}

                discount_data['Category'] = category_name

                discount_data['Image_link_visible'] = discount_item.find_element(By.TAG_NAME, value="img").get_attribute("src")
                discount_data['Image_link'] = discount_item.find_element(By.TAG_NAME, value="img").get_attribute("data-src")

                try:
                    discount_data['Discount_icon_text'] = discount_item.find_element(By.TAG_NAME, value="h3").get_attribute("textContent")
                except:
                    discount_data['Discount_icon_text'] = None

                discount_data['Item_name'] = discount_item.find_element(By.TAG_NAME, value="h4").get_attribute("textContent")

                try:
                    discount_data['Item_discount_time'] = discount_item.find_element(By.CLASS_NAME, value="offer-dateTo-wrapper").get_attribute("textContent")
                except:
                    discount_data['Item_discount_time'] = None
                try:
                    discount_data['Discount_shop_size'] = len(discount_item.find_elements(By.CLASS_NAME, value="x-icon"))
                except:
                    discount_data['Discount_shop_size'] = None

                discount_data['Item_price_euro'] = discount_item.find_element(By.CLASS_NAME, value="price-eur").get_attribute("textContent")
                discount_data['Item_price_cents'] = discount_item.find_element(By.CLASS_NAME, value="price-cents").get_attribute("textContent")

                try:
                    discount_data['Item_price_before'] = discount_item.find_element(By.CLASS_NAME, value="text-decoration-line-through").get_attribute("textContent")
                except:
                    discount_data['Item_price_before'] = None

                try:
                    discount_facilitator = discount_item.find_element(By.CLASS_NAME, value="offer-bottom-icon-wrapper")
                    discount_data['Discount_facilitator'] = discount_facilitator.find_element(By.TAG_NAME, value="img").get_attribute("alt")
                except:
                    discount_data['Discount_facilitator'] = None
                self.data.append(discount_data)

    def execute_scraper(self):
        """Executes the scraper logic.
        """
        print("Starting Maxima Discount Scraper")
        self.scrape_maxima(self.get_driver())
        df = self.postprocessing(self.data)
        self.upload(df)
        print("Maxima Discount Scraper finished")


if __name__ == '__main__':
    MaximaScraper(str(date.today())).execute_scraper()