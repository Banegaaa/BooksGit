from bs4 import BeautifulSoup
import requests
import csv


def find_books(): 
    with open('result.csv', 'w', newline='',encoding='utf-8') as my_file:
        field_names = ['title', 'author', 'rating', 'format', 'price']
        the_writer = csv.DictWriter(my_file, fieldnames=field_names)
        the_writer.writeheader()
        
        page = 1
        while True:
            url = "https://www.bookdepository.com/search?searchTerm=python&category=1708&page={}".format(str(page))
        
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'lxml')
        
            books = soup.find_all('div', class_="book-item")
            
            if books:
                
                for book in books:
                    #Scraping the title
                    book_name = book.find('h3', class_ ='title').text.strip()
                    
                    #Scraping the author
                    author_name = book.find('p', class_ = 'author').text.strip()
               
                    #Calculating the rating
                    full_stars = book.find_all('span', class_ = 'star full-star')
                    half_star = book.find('span', class_ = 'star half-star')
                    num_stars = 0
                    for star in full_stars:
                        num_stars += 1
                    if half_star:
                        num_stars += 0.5
                    num_stars = str(num_stars)  
                    
                    #Scraping the format
                    format_ = book.find('p', class_ = 'format').text.strip()
                   
                    #Scraping the price
                    price = book.find('p', class_ = "price")
                    old_price = book.find('span', class_='rrp')
                    discount = book.find('p', class_='price-save')
                    if old_price:
                        new_price = round(calculate_price(old_price.text.split()[0]) - calculate_price(discount.text.split()[1]),2)
                    else:
                        if price:
                            new_price = round(calculate_price(price.text.strip().split()[0]),2)
                        else:
                            new_price = 'Unavailable'                    
                    
                    #Write a new row
                    the_writer.writerow({'title': book_name, 'author': author_name, 'rating' : num_stars, 'format' : format_, 'price' : new_price})
                    
                page += 1
            else:
                break
            
def calculate_price(price_string):
    int_ = int(price_string.split(',')[0])
    decimal = int(price_string.split(',')[1])
    price = int_ + decimal/100
    return price
    

if __name__ =='__main__':
    find_books()

