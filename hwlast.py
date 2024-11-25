import requests
from bs4 import BeautifulSoup

# Базовий URL
base_url = "http://books.toscrape.com/catalogue/"


# Функція для отримання книг зі сторінки
def get_books_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    books = soup.find_all('article', class_='product_pod')

    book_data = []
    for book in books:
        title = book.h3.a['title']  # Назва книги
        price = book.find('p', class_='price_color').text  # Ціна книги
        book_data.append({'title': title, 'price': price})
    return book_data


# Перебір усіх сторінок
def get_all_books(base_url):
    books = []
    for i in range(1, 51):  # Підозрюємо, що 50 сторінок максимум
        page_url = f"{base_url}page-{i}.html"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, features="html.parser")

        # Перевірка, чи сторінка існує
        page = soup.find("li", {"class": "current"})
        if not page:  # Якщо сторінки немає, виходимо з циклу
            break

        print(f"Завантаження сторінки: {page.text.strip()}")
        books.extend(get_books_from_page(page_url))
    return books


# Виконання скрипта
all_books = get_all_books(base_url)

# Виведення результатів
print(f"Усього книг знайдено: {len(all_books)}")
for book in all_books:
    print(f"Назва: {book['title']}, Ціна: {book['price']}")