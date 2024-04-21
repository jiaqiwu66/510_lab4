# Book Scraper
## Overview
A webapp to scraper the books information, store in the Supabase. User can search by name and description, filter and order by rating/price in the Streamlit app.

View my web app at: https://510lab4-jmqmgmdzocdvnskrtngqxj.streamlit.app/


Contains 3 parts:

- Search bar for name and description.
- Filter and order by price and rating.
- The data table of 1000 books.

## Getting Started
- Create ```quotes_scraper.py``` to scrap data from the URL.
- Use ```create_table``` function in ```db.py``` to create a table in the existing database.
- Create a streamlit app to present the table and other functions.

## Lessons Learned
- Run the ```quotes_scraper.py``` before ```streamlit run app.py```, or you can't get data.
- Remember to install the beautifulsoup4 both via ```pip install``` and in ```requirements.txt```.
- The "description" is in a subpage, so I use this to scrape:
    ```
    link = book_article.select_one('h3').select_one('a').get('href')
    sub_url = BASE_URL.format(route=link)
    print(f"Scraping {sub_url}")
    sub_response = requests.get(sub_url)
    sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
    ```
- Some books don't have a description, to avoid error, I use this:
    ```
    if len(p_list) == 0:
        book["description"] = ""
    else:
        book["description"] = p_list[0].text
    ```
- The rating in element is in text format, but can convert it into float use this:
    ```
    RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    ```

- Sometimes if search result is none will lead to erroe. To avoid this, I use:
    ```
    if len(pages) == 0:
        st.write("No books available")
    else:
        container.dataframe(data=pages[current_page - 1], use_container_width=True)
    ```
- When design the search for name or description, can use this:
    ```
     if search_term:
            df = pd.read_sql
            (f"SELECT * FROM books "
             f"WHERE name ILIKE '% {search_term}%' "
             f"ORDER BY created_at DESC", pg.con)
    ```
    - Use ```ILIKE``` to ignore capitals and lower case.
    - Add a space between```%``` and  ```{search_term}```to ensure the search accuracy for a word.
- Not forget to set secret in streamlit

## Question
- Still curious about why the data storage breaks can be resolved by using ```pg.truncate_table()```
## Todo
- How to scraper the data on a real time website?