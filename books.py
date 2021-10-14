from bs4 import BeautifulSoup
import requests
import csv

html_text = requests.get("https://www.bookdepository.com/search?searchTerm=python&category=1708&page=1").text
soup = BeautifulSoup(html_text, 'lxml')

with open('pythonBooks.csv', 'w', newline='') as myFile:
    fieldNames = ['title', 'author', 'rating', 'format', 'price']
    theWriter = csv.DictWriter(myFile, fieldnames=fieldNames)
    theWriter.writeheader()
    
    books = soup.find_all('div', class_="book-item")

    for book in books:
        book_name = book.find('h3', class_ ='title').text.strip()
        author_name = book.find('p', class_ = 'author').text
   
        full_stars = book.find_all('span', class_ = 'star full-star')
        half_star = book.find('span', class_ = 'star half-star')
        num_stars = 0
        for star in full_stars:
            num_stars += 1
        if half_star:
            num_stars += 0.5
        num_stars = str(num_stars) + "/5"    
        
        format_ = book.find('p', class_ = 'format').text
       
        price = book.find('p', class_ = 'price')
        if price:
            price = price.text.replace(' ', '').split()
            price = price[0]
        elif not price:
            price = "Unavailable"
    
        theWriter.writerow({'title': book_name, 'author': author_name.strip(), 'rating' : num_stars, 'format' : format_.strip(), 'price' : price})

