import requests
from bs4 import BeautifulSoup

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
          'referer':'https://www.zillow.com/mt/rentals/apartament'}



urlDpto = 'https://www.zillow.com/mt/rentals/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A49.64739445340297%2C%22south%22%3A43.645258592201124%2C%22east%22%3A-103.88145292187501%2C%22west%22%3A-116.20811307812501%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A35%2C%22regionType%22%3A2%7D%5D%2C%22filterState%22%3A%7B%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A7%2C%22usersSearchTerm%22%3A%22Montana%22%2C%22schoolId%22%3Anull%2C%22pagination%22%3A%7B%7D%7D'

urlCasa = 'https://www.zillow.com/mt/houses/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A49.64739445340297%2C%22south%22%3A43.645258592201124%2C%22east%22%3A-103.88145292187501%2C%22west%22%3A-116.20811307812501%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A35%2C%22regionType%22%3A2%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A7%2C%22usersSearchTerm%22%3A%22Montana%22%2C%22schoolId%22%3Anull%2C%22pagination%22%3A%7B%7D%7D'


urls = [urlDpto, urlCasa]
types = ['Apartment', 'House']
subtypes = ['For rent', 'For sale']


with open("zillow.csv", "w") as f:
    f.write("Tipo; Precio; Subtipo; Dirección\n")


for url, tipo, subtype in zip(urls, types, subtypes):
    next_url = url
    while next_url:
        data = requests.get(next_url, headers=header)
        soup = BeautifulSoup(data.text, 'lxml')

        price = soup.find_all('span', {'data-test':'property-card-price'})
        address = soup.find_all('address', {'data-test':'property-card-addr'})

        pr=[]
        adr=[]
        for result in price:
            pr.append(result.text)
        for result in address:
            adr.append(result.text)

        with open("zillow.csv", "a") as f:
            for i in range(len(pr)):
                f.write(tipo + "; " + str(pr[i]) + "; " + subtype + "; " + str(adr[i]) + "\n")

        # Encuentra la URL de la siguiente página
        next_page = soup.find('a', {'rel':'next'})  # Busca un elemento 'a' con el atributo 'rel' establecido en 'next'
        next_url = 'https://www.zillow.com' + next_page['href'] if next_page else None