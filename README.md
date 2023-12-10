# maxima-discount-scraper
A scraper designed to obtain data from [Maxima discount website](https://www.maxima.lt/akcijos).

## Let's GO
I have come back to this project after almost 2 years, and am planning on finally finishing it. I have rebuilt the scraper to account for the new website and will automate the scraping with AWS server.

## Functionality:
Obtains the following data on every item:
1. Item image url
2. Discount icon text
3. Item name
4. Item discount time
5. Discount shop size
6. Item price euro
7. Item price cents
8. Discount text decorator
9. Discount facilitator

## Usage:

The [scraperv2.py](scraperv2.py) has to be run in the environment that has the folowing modules installed:
1. pandas
2. numpy
3. Selenium
4. requests

The scraper was created for personal use so there are no test that would ensure the data is collected properly, if the site structure changed the scraper would not work and return an empty csv file. I will be working on tests in the future.

That said, you are welcome to fork and work on improving this scraper :), and if there are any improvement that you would like to see do not hesitate to contact me.

## Possible errors:

1. Could not reach the site - there may be a problem with requests library or the site is down.
2. Some execution error - the code could be too old or the site structure could have been changed, do not hesitate to message me about problems.
