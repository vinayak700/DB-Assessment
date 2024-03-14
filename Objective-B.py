# Objective: Scrape books data from http://books.toscrape.com and store it in Database.

from bs4 import BeautifulSoup
import urllib.request as ur
from connection import db

# URL of the website to scrape
urlinput = "https://books.toscrape.com"

# Function to extract book information from the webpage.
def get_books(urlinput):
    def extract_book_info(book_tag):
        #Function to extract book information from each book tag.
        book = {}
        book['name'] = book_tag.h3.a['title']
        book['price'] = book_tag.find('p', class_='price_color').get_text()
        book['image'] = book_tag.img['src']
        book['availability'] = book_tag.find('p', class_='instock availability').get_text().strip()
        book['rating'] = book_tag.find('p', class_='star-rating')['class'][1]
        return book

    s = ur.urlopen(urlinput)
    soup = BeautifulSoup(s.read(), 'html.parser')
    book_tags = soup.find_all('article', class_='product_pod')

    books = []
    for book_tag in book_tags:
        books.append(extract_book_info(book_tag))

    return books

#Function to fetch all books from the website.
def get_all_books():
    all_books = []
    print(f"Fetching books from {urlinput}")
    print("Fetching in progress...")
    print("Please wait...")

    current_page = 1
    while current_page <= 50:
        url = f"{urlinput}/catalogue/page-{current_page}.html"
        books_on_page = get_books(url)
        if not books_on_page:
            break
        all_books.extend(books_on_page)
        current_page += 1

    print("Books have been fetched!!")
    return all_books

#Function to store fetched books in the database.
def store_books():
    all_books = get_all_books()
    db.books.insert_many(all_books)
    print('Books have been added to the database.')

if __name__ == '__main__':
    store_books()
