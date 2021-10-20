import argparse
from bs4 import BeautifulSoup
import requests
import csv
import os

CSV_FILE_LOC = os.environ.get('CSV_FILE_LOCATION')


class BadCategoryException(Exception):
    pass


def find_books(category, search_term):
    with open(CSV_FILE_LOC, 'w', newline='', encoding='utf-8') as my_file:
        field_names = ['title', 'rating', 'price']
        the_writer = csv.DictWriter(my_file, fieldnames=field_names)
        the_writer.writeheader()

        if category == "TGI":
            category_code = 1709
        elif category == "TTT":
            category_code = 1842
        else:
            raise BadCategoryException

        page = 1
        while True:
            url = "https://www.bookdepository.com/search?searchTerm={}&category={}&page={}".format(search_term, str(category_code), str(page))
        
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'lxml')
        
            books = soup.find_all('div', class_="book-item")
            
            if books:
                
                for book in books:
                    # Scraping the title
                    book_name = book.find('h3', class_='title').text.strip()
                    
                    # Scraping the author
                    # author_name = book.find('p', class_='author').text.strip()
               
                    # Calculating the rating
                    full_stars = book.find_all('span', class_='star full-star')
                    half_star = book.find('span', class_='star half-star')
                    num_stars = 0
                    for star in full_stars:
                        num_stars += 1
                    if half_star:
                        num_stars += 0.5
                    num_stars = str(num_stars)  
                    
                    # Scraping the format
                    # format_ = book.find('p', class_ ='format').text.strip()
                   
                    # Scraping the price
                    price = book.find('p', class_="price")
                    old_price = book.find('span', class_='rrp')
                    discount = book.find('p', class_='price-save')
                    if old_price:
                        new_price = round(calculate_price(old_price.text.split()[0]) - calculate_price(discount.text.split()[1]),2)
                    else:
                        if price:
                            new_price = round(calculate_price(price.text.strip().split()[0]),2)
                        else:
                            new_price = 'Unavailable'                    
                    
                    # Write a new row
                    the_writer.writerow({'title': book_name, 'rating': num_stars, 'price': new_price})
                    
                page += 1
            else:
                break


def calculate_price(price_string):
    int_ = int(price_string.split(',')[0])
    decimal = int(price_string.split(',')[1])
    price = int_ + decimal/100
    return price
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", dest="category", required=True, help="Category for search")
    parser.add_argument("-s", dest="search_term", required=True, help="Search term")
    args = parser.parse_args()
    try:
        find_books(args.category, args.search_term)
    except BadCategoryException:
        print("Invalid category selected")
