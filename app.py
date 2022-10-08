from bs4 import BeautifulSoup
import requests
import sqlite3

baseurl = 'https://www.thewhiskyexchange.com'

#using https://www.whatismybrowser.com/detect/what-is-my-user-agent/
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

db = sqlite3.connect('database.db')

cursor = db.cursor()

command1 = '''CREATE TABLE IF NOT EXISTS products(
    name  PRIMARY KEY,
    description TEXT,
    price REAL
)'''

cursor.execute(command1)
db.commit()
cursor = db.cursor()

#loop through all of three pages
for x in range(1,3):
    r = requests.get(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={x}')
    soup = BeautifulSoup(r.content, 'lxml')
    productnamelist = soup.find_all('a', class_ = 'product-card')
    for item in productnamelist:
        name = item.find('p', class_ = 'product-card__name').text.strip()
        description = item.find('p', class_ = 'product-card__meta').text.strip()
        price = item.find('p', class_ = 'product-card__price').text.strip()
        #print(name + '\n' + description + '\n' + price + '\n\n')
        command2 = '''INSERT INTO products(name, description, price) VALUES(?,?,?)'''
        cursor.execute(command2, (name, description, price))
        db.commit()

cursor.execute('''SELECT * FROM products''')
products1 = cursor.fetchall()
print(len(products1))

db.close()
