from bs4 import BeautifulSoup

def getCityLinks(html):
    soup = BeautifulSoup(html, "html.parser")

    countryNames = ['Serbia']
    countries = soup.find_all("div", {'class' : 'card'})
    cities = [city.h4.a['href'] for country in countries for city in country.div.ul.findChildren('li') if city.h4.a['data-gtm-country'] in countryNames]

    return cities



