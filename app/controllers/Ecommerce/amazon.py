#!C:/bin
from selenium.webdriver.common.by import By
from selenium.common.exceptions import SessionNotCreatedException
from app.controllers.Ecommerce.driver_config import set_driver_config
from bs4 import BeautifulSoup


# url = "https://www.amazon.com/Bulova-Two-Tone-Stainless-Chronograph-Bracelet/product-reviews/B0713STW5H/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

# def begin_amazon_search(url):
#     """Takes the url of the product review page and recursively get the review"""
#     search_result =[]
#     driver = set_driver_config() #get the driver from the config
#     def get_page_source(url):
#         #print(url)
#         driver.get(url)

#         element_text = driver.page_source

#         result = amazon_beautiful_soup_search(element_text) #calling the beautifulsoup method to extract the text

#         search_result.append(result) #appending the result to the initial value

#         try:
#             next_page = driver.find_element(By.PARTIAL_LINK_TEXT,'Next')
#         except:
#             driver.quit()
#             return search_result

#         if next_page is not None:
#             value= next_page.get_attribute('href')
#             url = value
#             get_page_source(url) #calling the function in it self until the if condition fails
#         driver.quit()
#     get_page_source(url)
#     return search_result


def begin_amazon_search(url):
    try:
        driver = set_driver_config()
    except SessionNotCreatedException as e:
        return {"msg": f"{e.msg} please try again"}

    search_result = []
    n = 0
    while n <= 2:
        driver.get(url)
        element_text = driver.page_source
        result = amazon_beautiful_soup_search(element_text)
        # search_result.append(
        #     result
        # )  # calling the beautifulsoup method to extract the text
        search_result.extend(result)

        next_page = driver.find_element(By.PARTIAL_LINK_TEXT, "Next")
        value = next_page.get_attribute("href")
        url = value
        n += 1
    driver.quit()
    return search_result


def amazon_beautiful_soup_search(resp):

    data_str = ""

    soup = BeautifulSoup(resp, "html.parser")
    review_date = soup.findAll(
        "span", class_="a-size-base a-color-secondary review-date"
    )
    review_text = soup.findAll(
        "span", class_="a-size-base review-text review-text-content"
    )

    for item_date, item_text in zip(review_date, review_text):
        date = item_date.get_text().strip("\n")
        text = item_text.get_text().strip("\n")
        sentence = text + ">" + date
        data_str = data_str + f"{sentence}" + "\n"
        # print(data_str)
    result = data_str.split("\n")

    return result


# span class_="a-size-base a-color-secondary review-date"
