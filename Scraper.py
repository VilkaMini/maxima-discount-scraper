import requests
from bs4 import BeautifulSoup
import string
import pandas as pd
from datetime import date

info = {
    "item_name": [],
    "eur_after_dc": [],
    "cents_after_dc": [],
    "price_before_dc": [],
    "discount_percent": [],
    "description_ad": [],
    "image_url": [],
    "special_badge_url": [],
}

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://www.maxima.lt/akcijos"
array_of_keys = list(info.keys())

# Get site info
try:
    page = requests.get(url, headers=headers)
except Exception as e:
     raise Exception("Could not reach the site") from e

# Make soup from html
soup = BeautifulSoup(page.content, "html.parser")

# Going though individual items
for item in soup.find_all("div", class_="offer-page-sale-item offer-page-sale-item__actual"):
    # Creating a dictionary to put all item's info
    temp_info = {
        "item_name": [],
        "eur_after_dc": [],
        "cents_after_dc": [],
        "price_before_dc": [],
        "discount_percent": [],
        "description_ad": [],
        "image_url": [],
        "special_badge_url": [],
    }

    # Taking image
    img_div = item.find("div", class_="img")
    temp_info["image_url"] = "https://www.maxima.lt" + str(img_div.find("img")["src"])
    temp_info["item_name"] = item.find("div", class_="title").text
    # Checking if description exists
    if item.find("div", class_="desc"):
        temp_info["description_ad"] = item.find("div", class_="desc").text
    # Checking if price is bare
    if item.find("div", class_="discount price bare"):
        # Taking bare value
        temp_info["eur_after_dc"] = item.find("span", class_="value").text
        temp_info["cents_after_dc"] = item.find("span", class_="cents").text
    # If price not bare
    else:
        # Checking if only discount is on display
        if item.find("div", class_="discount percents"):
            temp_info["discount_percent"] = item.find("span", class_="value").text
        else:
            t1 = item.find("div", class_="t1")
            temp_info["eur_after_dc"] = t1.find("span", class_="value").text
            temp_info["cents_after_dc"] = t1.find("span", class_="cents").text
            # Checking if extra banner exists
            if item.find("div", class_="t1_1 t1_1_blue"):
                banner = item.find("div", class_="t1_1 t1_1_blue")
                temp_info["special_badge_url"] = "https://www.maxima.lt" + str(banner.find("img")["src"])
            # Checking if price before is specified
            if item.find("div", class_="t2"):
                t2 = item.find("div", class_="t2")
                temp_info["price_before_dc"] = t2.find("span", class_="value").text

    # Copying info from temporary storage to info dict and populating not existing values with none's
    for i in range(len(array_of_keys)):
        if not temp_info[array_of_keys[i]]:
            info[array_of_keys[i]].append(None)
        else:
            info[array_of_keys[i]].append(temp_info[array_of_keys[i]])

df = pd.DataFrame(info)

df.to_csv(f"{date.today()}-maxima.csv", encoding='utf-16')