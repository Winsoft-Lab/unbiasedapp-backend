from facebook_scraper import get_posts_by_search, get_posts
import browser_cookie3


def search_facebook(query, page_num):
    cookie=browser_cookie3.load()
    result = []
    for post in get_posts_by_search(query, cookies='from_browser' , extra_info=True, options={'comments':True}, pages=page_num):
        result.append(post)

    return result


def scrape_facebook_page(page_name, page_num):
    cookie = browser_cookie3.load()
    result = []
    for post in get_posts(page_name, cookies='from_browser' , extra_info=True, options={'comments':True}, pages=page_num):
        result.append(post)
    return result