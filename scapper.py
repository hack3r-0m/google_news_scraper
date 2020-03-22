from bs4 import BeautifulSoup
import sys
from requests import get, ConnectionError
import csv
import time

class Main():

    def __init__(self):
        self.useragent = { 'useragent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.24 (KHTML, like Gecko) Iron/11.0.700.2 Chrome/11.0.700.2 Safari/534.24'
                        }
        self.special_words = [ 'corona',
                                'virus',
                                'Coronavirus'
                                'COVID-19',
                                'slowdown',
                                'surge',
                                'quarantine',
                                'deaths',
                                'cases',
                                'lockdown',
                                'IPO',
                                'acquisitions'
        ]

    def build_connection(self):
        google_news_url = 'https://news.google.com/?hl=en'
        response = get(google_news_url, headers=self.useragent)

        if response.status_code != 200:
            raise ConnectionError("Expected status code 200, but got {}".format(response.status_code))

        return response

    def build_scrapper(self, response):

        raw_soup = BeautifulSoup(response.text, "lxml")

        all_news = list()

        # gets both primary and secondary news together
        for news in raw_soup.find_all('a', attrs={'class': 'DY5T1d'}):
            all_news.append(news.text)

        return all_news
 
    def result_purifier(self, all_news):

        for word in self.special_words:
            for news in all_news:
                for news_word in news.split(" "):

                    if word.lower() == news_word.lower():

                        moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime()) # for creating new csv everytime script is executed

                        with open('output'+moment+'.csv', 'a+', newline='') as board: # newline attribute for omitting blank lines in csv gile
                            writer = csv.writer(board)
                            writer.writerow([word,news])
                            board.close()

        return None

if __name__ == '__main__':
    instance = Main()
    connection = instance.build_connection()
    scrapped_data = instance.build_scrapper(connection)
    output = instance.result_purifier(scrapped_data)

    print("Process completed! check the output CSV file")
    sys.exit()
