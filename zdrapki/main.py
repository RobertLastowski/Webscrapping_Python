import requests
import bs4


#   function for creating list of links for separate "zdrapka" page
def get_links():
    # main url to home page
    lotto_url = "https://www.lotto.pl"
    res = requests.get("https://www.lotto.pl/zdrapki/katalog-zdrapek")
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    links = []
    # loop for gathering all "zdrapka" type items partly urls
    for link in soup.find_all("div", class_="scratch-card-item__name"):
        for a in link.find_all("a"):
            links.append(a['href'])

    # for link in links:
    #     links[links.index(link)] = lotto_url + link


    # loop that create a list of whole urls to every single "zdrapka" type item in the catalog
    for num in range(len(links)):
        links[num] = lotto_url + links[num]

    return links


def scrapper():
    links = get_links()
    for link in links:
        num_win = 0
        num_to_win = 0
        res = requests.get(url=link, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
        if res.status_code == 200:
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            title = soup.find('div', class_="scratch__title")
            # # PRICE DOES NOT WORK, IT'S NOT READING HARD SPACE SYMBOLS BETWEEN NUMBER
            price_step = soup.find('div', class_="scratch__price")
            price = price_step.find("strong").text.split('\xa0')
            print(f"cena:{price}")

            prize_number = soup.find_all('div', class_="scratch__mobile-row")
            for item in prize_number:
                if item.find("span").text == "Liczba wygranych":
                    num_win += int(item.find("strong").text)
                if item.find("span").text == "Pozostało do wygrania":
                    num_to_win += int(item.find("strong").text)
            print(
                f"{title.text}\nLiczba wygranych: {num_win} \nPozostało do wygrania:{num_to_win}\nProcent wygranych na rynku:{num_to_win / num_win}\n\n")
        else:
            print("blad :C")


if __name__ == '__main__':
    scrapper()
