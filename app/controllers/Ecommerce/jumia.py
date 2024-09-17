#!C:/bin

from selenium.webdriver.common.by import By
from app.controllers.Ecommerce.driver_config import set_driver_config
from bs4 import BeautifulSoup


# url = 'https://www.jumia.com.ng/catalog/productratingsreviews/sku/ED473EA1DPCYRNAFAMZ/'


def begin_jumia_search(url):
    """Takes the url of the product review page and recursively get the review"""
    search_result = []
    driver = set_driver_config()

    def get_page_source(url):
        driver.get(url)
        element_text = driver.page_source

        result = jumia_beautiful_soup_search(
            element_text
        )  # calling the beautifulsoup method to extract the text

        # search_result.append(result)  # appending the result to the initial value
        search_result.extend(result)
        try:
            next_page = driver.find_element(
                By.CSS_SELECTOR, "a[aria-label='Next Page']"
            )
        except:
            driver.quit()
            return search_result

        if next_page is not None:
            value = next_page.get_attribute("href")
            url = value
            get_page_source(
                url
            )  # calling the function in it self until the if condition fails

    get_page_source(url)
    return search_result


def jumia_beautiful_soup_search(resp):

    data_str = ""

    soup = BeautifulSoup(resp, "html.parser")
    for item in soup.findAll(
        "article", class_="-pvs -hr _bet"
    ):  # Has class -pvs -hr _bet from jumia with the aritcle tag
        data_str = data_str + item.get_text() + "\n"
    result = data_str.split("\n")

    return result
