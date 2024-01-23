## Amazon Matcha Scrapper
## Thomas Gonzalez
## Tested and ran successfully on 1/22/2024

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
s = HTMLSession()
dealsList = []

## Creates search term for product
searchTerm = 'matcha+green+tea+powder'
url = 'https://www.amazon.com/s?k={searchTerm}'

##Intializes the beautiful soup object 
def searchData(url):

    r = s.get(url)
    # to make sure the bot doesnt get kicked out from amazon servers
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

## Utilizes for loops to obtain the prices, reviews, titles on the page and compare them to the old versions and appends them to the master list (dealsList). While utilizing a try, excecpt to ensure no errors arise
def getDiscount(soup):

    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    for item in products:
        title = item.find('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()
        shortTitle = item.find('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()[:25]
        link = item.find('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']

        try:
            salePrice = float(item.find_all('span', {'class': 'a-offscreen'})[0].text.replace('$','').strip())
            oldPrice = float(item.find_all('span', {'class': 'a-offscreen'})[1].text.replace('$','').strip())
        except:
            oldPrice = float(item.find('span', {'class': 'a-offscreen'})[1].text.replace('$','').strip())

        try:
            reviews = float(item.find('span', {'class': 'a-size-base'}).text.strip())
        except:
            reviews = 0


        saleItem = {
            'title': title,
            'shortTitle': shortTitle,
            'link': link,
            'salesPrice': salePrice,
            'oldPrice': oldPrice,
            'reviews': reviews
        } 
        dealsList.append(saleItem)

##Allows for the bot to go from one page to the next using variable pages
def getNextPage(soup):
    pages = soup.find('ul', {'class': 'a-pagination'})
    if not pages.find('li', {'class': 'a-disabled a-last'}).find('a')['href']:
        url = 'https://www.amazon.co.us' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return

##Loop intializes the function getDiscount and getNextPage to go through all the various products and pages availible under any given search term.
while True:
    data = getDiscount(url)
    getDiscount(data)
    url = getNextPage(soup)
    if not url:
        break
    else:
        print(url)
        print(len(dealsList))

##Utilizing panda, the bot puts our data optained from our master list, and adds a new discount percentage while also placing it in a readable CSV file for later use.
df = pd.DataFrame(dealsList)
df['percentOff'] = 100 - ((df.salePrice / df.oldPrice)*100)
df = df.sort_values(by=['percentOff'], ascending = False)
df.to_csv('matchaDeals.csv', index = False)
print('Completed.')


    