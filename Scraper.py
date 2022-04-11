import os
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import *

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://www.maxima.lt/akcijos"

def main():
    """Scrapes the maxima website for discounts"""
    info = get_array()
    array_of_keys = list(info.keys())

    page = get_site()
    soup = BeautifulSoup(page.content, "html.parser")

    # Going though individual items
    for item in soup.find_all("div", class_="card-body offer-card d-flex flex-column justify-content-between"):
        # Creating a dictionary to put all item's info
        temp_info = get_array()
        # Taking image
        img_div = item.find("div", class_="offer-image w-100 d-flex justify-content-center position-relative")
        temp_info["image_url"] = img_div.find("img")["data-src"]
        temp_info["item_name"] = (item.find("h4", class_="mt-4 text-truncate text-truncate--2 align-self-end").text).replace('\n', '')
        # Taking bare value
        temp_info["eur_after_dc"] = (item.find("div", class_="price-eur").text).replace('\n', '')
        temp_info["cents_after_dc"] = (item.find("span", class_="price-cents h-50").text).replace('\n', '')
        # Checking if old price exists
        if item.find("div", class_="price-old h-50 ms-1"):
            # Discount banner
            disc = item.find("div", class_="discount-icon")
            if disc.find("img"):
                temp_info["special_badge_url"] = disc.find("img")['src']
            else:
                temp_info["discount_percent"] = (disc.find("h3").text).replace('\n', '')
            # Price before
            temp_info["price_before_dc"] = (item.find("span", class_="text-decoration-line-through").text).replace('\n', '')

        info = copy_to_dict(array_of_keys, temp_info, info)

    create_file(info)
    return 0

def get_array() -> dict:
    """Returns a dictionary used to hold discount information
    
    Parameters:
        none.
    
    Returns:
        iarray: A dictionary with keys to arrays to hold information.
    """
    iarray = {
        "item_name": [],
        "eur_after_dc": [],
        "cents_after_dc": [],
        "price_before_dc": [],
        "discount_percent": [],
        "image_url": [],
        "special_badge_url": [],
    }
    return iarray

def get_site() -> requests.Response():
    """Gets information from Maxima site.

    Parameters:
        none.

    Returns:
        page (requests.Response): Object with information from site.
    """
    try:
        page = requests.get(url, headers=headers)
    except Exception as e:
        raise Exception("Could not reach the site") from e
    return page

def copy_to_dict(array_of_keys: np.array, temp_info: dict, info: dict) -> dict:
    """Appends new values to the dictionary from temporary dictionary.

    Parameters:
        array_of_keys (np.array): array of keys in dictionary.
        temp_info (dict): dictionary with values scanned from one website item.
        info (dict): dictionary with all existing items on the website.

    Returns:
        info (dict): dictionary with additional items from the website.
    """
    for i in range(len(array_of_keys)):
        if not temp_info[array_of_keys[i]]:
            info[array_of_keys[i]].append(None)
        else:
            info[array_of_keys[i]].append(temp_info[array_of_keys[i]])
    return info

def make_dataframe(info: dict) -> pd.DataFrame:
    """Makes given dictionary a dataframe.

    Parameters:
        none.

    Returns:
        info (pd.DataFrame): dataframe with all site information.
    """
    return pd.DataFrame(info)

def get_file_name():
    """Returns a file name based on discount date.

    Parameters:
        none.

    Returns:
        string (str): string with file name.
    """
    start = date(2021, 11, 2)
    days_passed = date.today() - start

    for _ in range(int(np.floor(days_passed.days / 7))):
        start += timedelta(days=7)

    return f"{start}-maxima-{start + timedelta(days=6)}.csv"

def create_file(info: dict) -> int:
    """Creates a file with discount information.

    Parameters:
        info (dict): information dictionary.

    Returns:
        int (int): status that the file was created successfully.
    """
    if not os.path.exists('files'):
        os.mkdir('files')

    df = make_dataframe(info)
    df.to_csv(f"files/{get_file_name()}", encoding='utf-16')
    return 0

if __name__ == "__main__":
    main()