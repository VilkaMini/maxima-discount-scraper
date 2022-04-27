# maxima-discount-scraper
A scraper designed to obtain data from [Maxima discount website](https://www.maxima.lt/akcijos).

## Functionality:
Obtains the following data from Maxima website:
  1. item imagine url
  2. item name
  3. price after discount (in euros and cents)
  4. discount icon (if it exists)
  5. discount percentage (if it exists)
  6. old price (if it exists)

## Usage:

The [Scraper.py](Scraper.py) has to be run in the environment that has the folowing modules installed:
  1. pandas
  2. numpy
  3. BeautifulSoup

The scraper was created for personal use so there are no test that would ensure the data is collected properly, if the site strucure changed the scraper would not work and return an empty csv file. I will be working on tests in the future.

## Possible errors:

1. Could not reach the site - there may be a problem with requests library or the site is down.
2. Some execution error - the code could be too old or the site structure could have been changed, do not hesitate to message me about problems.
