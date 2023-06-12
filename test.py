import requests
from bs4 import BeautifulSoup as soup
import csv

url = "https://store.steampowered.com/search/?filter=topsellers&os=win"
source = requests.get(url)
soup = soup(source.content, 'html.parser')

games = soup.find_all('div', {'class': 'responsive_search_name_combined'})


max_title_length = max(len(game.find('span', {'class': 'title'}).text) for game in games)

titles = [game.find('span', {'class': 'title'}).text for game in games]
prices = []
release_dates = []

for game in games:
        price_container = game.find('div', {'class': 'col search_price_discount_combined responsive_secondrow'})
        price = price_container.find('div', {'class': 'col search_price responsive_secondrow'})
        price_tag = price_container.find('strike')
        
        if price_tag:
            prices.append(price_tag.text.strip())
        elif price:
            prices.append(price.text.strip())
        else:
            prices.append("N/A")
        
        release_dates.append(game.find('div', {'class': 'col search_released responsive_secondrow'}).text.strip())

with open('steam_games.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Release Date'])  # Write header

    # Write game data row by row
    for title, price, release_date in zip(titles, prices, release_dates):
        writer.writerow([title, price, release_date])

print("Data saved to steam_games.csv successfully.")

#maaf pak saya gak paham kalo web nya tidak pakai page tapi scroll terus, sellenium saya error terus pak :(