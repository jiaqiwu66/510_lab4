import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from db import Database

load_dotenv()
BASE_URL = 'https://books.toscrape.com/catalogue/{route}'
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
with Database(os.getenv('DATABASE_URL')) as pg:
    pg.create_table()

    # TODO: use argparse to enable truncating table
    # pg.truncate_table()

    books = []
    page = 1

    while True:
        route = f"page-{page}.html"
        url = BASE_URL.format(route=route)
        print(f"Scraping {url}")
        response = requests.get(url)

        # if outside valid page range
        if '404 Not Found' in response.text:
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        # select all quote divs
        book_articles = soup.select('article.product_pod')

        for book_article in book_articles:
            # parse individual quote
            book = dict()
            book['name'] = book_article.select_one('h3').select_one('a').get('title')

            link = book_article.select_one('h3').select_one('a').get('href')
            sub_url = BASE_URL.format(route=link)
            print(f"Scraping {sub_url}")
            sub_response = requests.get(sub_url)
            sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
            p_list = sub_soup.select('article.product_page > p')
            if len(p_list) == 0:
                book["description"] = ""
            else:
                book["description"] = p_list[0].text

            book['price'] = float(book_article.select_one('div.product_price').select_one('p.price_color').text[2:])
            book['rating'] = RATING_MAP[book_article.select_one('p').get("class")[1]]

            # insert into database
            pg.insert_quote(book)
            books.append(book)
            # print(book)
        page += 1
        print()
    # print(books)
