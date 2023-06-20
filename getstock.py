# Importing necessary libraries
import requests
from bs4 import BeautifulSoup
import json
import csv

# Defining the list of stock symbols here
stocks = ['HP', 'SGP.AX', 'MSFT', 'KO', 'PEP']
# An empty list to store the scraped data
data = []

def getStock(symbol):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'}
    url = f'https://au.finance.yahoo.com/quote/{symbol}'
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    
    stock = {
        'symbol': symbol,
        'price' : soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text,
        'change' : soup.find('div', {'class':'D(ib) Mend(20px)'}).find_all('span')[0].text,
        'per_change' : soup.find('div', {'class':'D(ib) Mend(20px)'}).find_all('span')[1].text
    }
    return stock

# Looping through the stocks and retrieving data
for item in stocks:
    print("Getting:", item)
    data.append(getStock(item))

# Writing the scraped data to a JSON file
with open('stockdata.json', 'w') as f:
    json.dump(data, f)

# Writing the scraped data to a CSV file
# Extracting the header rows from the first dictionary in the list
fieldnames = data[0].keys()

with open('stockdata.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()  # Write the header row with fieldnames
    writer.writerows(data)  # Write the data rows

print('Done.')