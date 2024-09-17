from bs4 import BeautifulSoup
from .scrape_bee import scraping_bee_api


def html_parser(product_name, product_id, sub_domain):
    """
    A function that takes product_name and product_review_id
    scrapes the text-content and checks for a next page
    """

    page_num = 2  # next page number

    rev_result = []

    init_url = f"https://amazon.{sub_domain}/{product_name}/product-reviews/{product_id}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

    def recursive_search(url=init_url, page_num=page_num):
        """
        A recursive search of the web page for next page parameter to scrape reviews
        """
        data_str = ""
        resp = scraping_bee_api(url)

        soup = BeautifulSoup(resp, "html.parser")

        for item in soup.findAll(
            "span", class_="a-size-base review-text review-text-content"
        ):
            data_str = data_str + item.get_text()

        result = data_str.split("\n")

        for i in result:
            if i == "":
                pass
            else:
                rev_result.append(i)

        # Checks if this next page <a href="next_page">Next page</a> exist in parsed page.
        # if sub_domain =='com':
        href = f'<a href="/{product_name}/product-reviews/{product_id}/ref=cm_cr_getr_d_paging_btm_{page_num}?ie=UTF8&pageNumber={page_num}&reviewerType=all_reviews&pageSize=10">Next page<span class="a-letter-space"></span><span class="a-letter-space"></span><span class="larr"></span>→</a>'
        # href =f'<a href="/{product_name}/product-reviews/{product_id}/ref=cm_cr_arp_d_paging_btm_{page_num}?ie=UTF8&amp;pageNumber={page_num}&amp;reviewerType=all_reviews">Next page<span class="a-letter-space"></span><span class="a-letter-space"></span><span class="larr"></span>→</a>'
        # else:
        #     href =f'<a href="/{product_name}/product-reviews/{product_id}/ref=cm_cr_arp_d_paging_btm_{page_num}?ie=UTF8&amp;pageNumber={page_num}&amp;reviewerType=all_reviews">Next page<span class="a-letter-space"></span><span class="a-letter-space"></span>→</a>'
        nxt = href
        els = soup.find_all("a")

        for el in els:

            if str(el) == str(nxt):

                print(nxt)

                next_page = f"https://www.amazon.{sub_domain}/{product_name}/product-reviews/{product_id}/ref=cm_cr_arp_d_paging_btm_next_{page_num}?ie=UTF8&reviewerType=all_reviews&pageNumber={page_num}"

                recursive_search(url=next_page, page_num=page_num + 1)

    recursive_search(url=init_url, page_num=page_num)

    return rev_result
